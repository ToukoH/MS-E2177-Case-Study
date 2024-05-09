from dataclasses import dataclass
from liabilities import Liabilities
from hedging_product import HedgingProduct
import numpy as np
from scipy.optimize import minimize, LinearConstraint


@dataclass
class HedgingStrategy:
    def __init__(self, data_real, data_rn,
                 hedging_product: HedgingProduct,
                 liabilities: Liabilities,
                 optimization_type,
                 n_of_simulations=None):
        """

        Parameters
        ----------
        data --- real data describing all simulations 
        data_rn --- risk neutral data describing all simulations 
        hedging_product --- an instance of the HedgingProduct class
        liabilities --- an instance of the Liabilities class
        n_of_simulations --- number of the simulations paths that we consider
        """
        self.data_real = data_real
        self.data_rn = data_rn
        self.optimization_type = optimization_type

        self.hp = hedging_product
        self.products = self.hp.products

        self.liabilities = liabilities
        self.contracts = self.liabilities.contracts

        self.n_of_simulations = n_of_simulations

        self.market_rates_list = [] # calculated in _split_data call

        self.liabilities_cashflows_list = []
        self.products_cashflows_list = [] # cashflows for different possible products. Asset cashflows can be calculated with this and x

        self.assets_cashflows_list = [] 

        self.market_rates_rn_list = []
        self.discount_factors_rn_list = []

        self.yield_curve = []

        self._split_data()

        self.market_rates_list = self.market_rates_list[0:self.n_of_simulations] # Vlad: Trunctate data based on simulation length
        self.market_rates_rn_list = self.market_rates_rn_list[0:self.n_of_simulations] # Vlad: Trunctate data based on simulation length
        
        self.npv_liabilities = self.liabilities.calculate_npv(self.market_rates_rn_list, self.discount_factors_rn_list)
        #self.npv_liabilities = -3_000_000
        print('The liabilities npv is: ',self.npv_liabilities)

        self.product_prices = self.hp.calculate_npvs(self.yield_curve)
        print(self.product_prices)

        self._calculate_liab_product_cashflows() # calculate liability and product cashflows only once at the start

    def _split_data(self):
        # Real data
        trials = self.data_real['Trial'].iloc[-1]
        split_data = np.split(self.data_real, trials)

        # Risk neutral data
        trials_rn = self.data_rn['Trial'].iloc[-1]
        split_data_rn = np.split(self.data_rn, trials_rn)

        for subset in split_data:  # Loop through the split data (real data)
            market_rates = subset['ESG.Economies.EUR_DEM.NominalYieldCurves.SWAP.SpotRate(Govt; 1; 3)'] 
            self.market_rates_list.append(market_rates)

        for subset in split_data_rn: # Loop through the split data (risk neutral data)
            market_rates_rn = subset['SpotRate1']
            self.market_rates_rn_list.append(market_rates_rn)

            discount_factors_rn = subset['Deflator']
            self.discount_factors_rn_list.append(discount_factors_rn)

        # Extract the yield curve
        self.yield_curve = (self.data_real.iloc[0]).to_numpy()[1:]

    #@staticmethod
    def cashflows_target_function(self, cashflow):
        """
        This is a function that we want to optimize. Basically, if we have a resulting cashflow,
        this is the measure of it being good or bad.
        Parameters
        ----------
        cashflow --- resulting cashflow wrt Fennia

        Returns
        -------
        The resulting cashflow score.
        """

        cashflow = cashflow[1:] # Do we want to add the initial cash flow to the hedging logic
        #return sum([c * (-c) if c < 0 else c for c in cashflow])
        if self.optimization_type == 1:
            return -np.linalg.norm(np.minimum(cashflow, np.zeros(len(cashflow)))) # don't care about positive cashflows
        else:
            return np.sum(cashflow)

    def match_cashflows(self, x):
        """
        This is a function, calculating the average cashflow target function among simulations.
        ----------
        x --- distribution of assets that we buy

        Returns
        -------
        average cashflow score.

        """
        accumulated_result = []
        for i in range(self.n_of_simulations):
            liabilities_cashflow = self.liabilities_cashflows_list[i]
            assets_cashflow = x.dot(self.products_cashflows_list[i]) 
            resulting_cashflow = assets_cashflow + liabilities_cashflow
            #resulting_cashflow = np.divide(resulting_cashflow, np.power((1+self.yield_curve[0:12]), np.arange(0, 12))) # Discount
            accumulated_result.append(self.cashflows_target_function(resulting_cashflow))

        if self.optimization_type == 2:
            return -np.percentile(accumulated_result, 5)
        else:
            return -np.sum(accumulated_result)
        

    def optimize_cashflow_difference(self):
        if self.n_of_simulations is None:
            self.n_of_simulations = len(self.market_rates_list)
        else:
            self.n_of_simulations = min(self.n_of_simulations, len(self.market_rates_list))

        print("Optimization started.")
        #init_cashflow = np.sum([contract.size for contract in self.contracts])
        x_0 = np.zeros(len(self.products))
        # constraint = LinearConstraint(A=np.identity(len(x_0)), lb=zero_time_npv, ub=zero_time_npv)
        # asset_prices = [product.price for product in self.products] # prices of products could be also calculated like this
        # asset_prices = self.hp.calculate_npvs(self.yield_curve) # calculate npvs of products (assets)
        asset_prices = self.product_prices
        #constraint = ({'type': 'ineq', 'fun': lambda x: self.liabilities.size_of_contracts - x.dot(asset_prices)}, #-self.npv_liabilities init_cashflow , - npv_liabilities >= assets at t=0 (npv_liab is neg)
        constraint = ({'type': 'ineq', 'fun': lambda x: -self.npv_liabilities - x.dot(asset_prices)}, #-self.npv_liabilities init_cashflow , - npv_liabilities >= assets at t=0 (npv_liab is neg)
                    {'type': 'ineq', 'fun': lambda x: x}) # x >= 0
        #bnds = ((0, 1e10) for i in range(len(x_0)))
        opt = {'maxiter':2000}
        res = minimize(self.match_cashflows, x_0, constraints=constraint, tol=0.001, options=opt)
        print(res)
        return res.x  # returns the size of the asset portfolio

    def calculate_optimal_average_cashflows(self, x):
        """
        This is a function that produces and returns the average liabilities and assets cashflows
        for a given asset distribution x.
        Parameters
        ----------
        x --- asset distribution

        Returns
        -------
        Average cashflows of liabilities and assets as a tuple.
        """
        self.assets_cashflows_list = []
        for product_cashflow in self.products_cashflows_list:
            self.assets_cashflows_list.append(x.dot(product_cashflow))

        self.assets_cashflows_list = np.array(self.assets_cashflows_list)
        return np.average(self.liabilities_cashflows_list, axis=0), np.average(self.assets_cashflows_list, axis=0)
    
    def _calculate_liab_product_cashflows(self):
        """
        This is a function, calculating the liability and product cash flow lists.
        ----------

        """
        for market_rates in self.market_rates_list[:self.n_of_simulations]:
            kwargs = {'t_end': len(market_rates),
                      'market_rates': market_rates}
            self.liabilities_cashflows_list.append(self.liabilities.calculate_cashflows(market_rates))
            self.products_cashflows_list.append(np.array([product.calculate_payoff(**kwargs) for product in self.products]))


        self.liabilities_cashflows_list = np.array(self.liabilities_cashflows_list)
        self.products_cashflows_list = np.array(self.products_cashflows_list)


