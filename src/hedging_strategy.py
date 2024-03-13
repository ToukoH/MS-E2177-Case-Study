from dataclasses import dataclass
from liabilities import Liabilities
from hedging_product import HedgingProduct
import numpy as np
from scipy.optimize import minimize, LinearConstraint


@dataclass
class HedgingStrategy:
    def __init__(self, data,
                 hedging_product: HedgingProduct,
                 liabilities: Liabilities,
                 n_of_simulations=None):
        """

        Parameters
        ----------
        data --- data describing all simulations
        hedging_product --- an instance of the HedgingProduct class
        liabilities --- an instance of the Liabilities class
        n_of_simulations --- number of the simulations paths that we consider
        """
        self.data = data

        self.hp = hedging_product
        self.products = self.hp.products

        self.liabilities = liabilities
        self.contracts = self.liabilities.contracts

        self.n_of_simulations = n_of_simulations

        self.market_rates_list = []
        self.liabilities_cashflows_list = None
        self.assets_cashflows_list = None

    def split_data(self):
        trials = self.data['Trial'].iloc[-1]
        split_data = np.split(self.data, trials)

        for subset in split_data:  # Loop through the split data
            market_rates = subset['SpotRate1']  # Using forecasted spot rates as the market rates
            self.market_rates_list.append(market_rates)

    @staticmethod
    def cashflows_target_function(cashflow):
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
        return np.linalg.norm(cashflow)

    def match_cashflows(self, x):
        """
        This is a function, calculating the average cashflow target function among simulations.
        ----------
        x --- distribution of assets that we buy

        Returns
        -------
        average cashflow score.

        """
        accumulated_result = 0
        for market_rates in self.market_rates_list[:self.n_of_simulations]:
            kwargs = {'t_end': len(market_rates),
                      'market_rates': market_rates}
            liabilities_cashflow = self.liabilities.calculate_cashflows(market_rates)
            assets_cashflow = x.dot(np.array([product.calculate_payoff(**kwargs) for product in self.products]))
            resulting_cashflow = assets_cashflow + liabilities_cashflow
            accumulated_result += self.cashflows_target_function(resulting_cashflow)
        return accumulated_result / self.n_of_simulations

    def optimize_cashflow_difference(self):
        self.split_data()
        if self.n_of_simulations is None:
            self.n_of_simulations = len(self.market_rates_list)
        else:
            self.n_of_simulations = min(self.n_of_simulations, len(self.market_rates_list))
        print("Optimization started.")
        x_0 = np.zeros(len(self.products))
        # constraint = LinearConstraint(A=np.identity(len(x_0)), lb=zero_time_npv, ub=zero_time_npv)
        bnds = ((0, 1e10) for i in range(len(x_0)))
        res = minimize(self.match_cashflows, x_0, tol=1)
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
        self.liabilities_cashflows_list = []
        self.assets_cashflows_list = []
        for market_rates in self.market_rates_list[:self.n_of_simulations]:
            kwargs = {'t_end': len(market_rates),
                      'market_rates': market_rates}
            self.liabilities_cashflows_list.append(self.liabilities.calculate_cashflows(market_rates))
            self.assets_cashflows_list.append(x.dot(np.array([product.calculate_payoff(**kwargs) for product in self.products])))
        self.liabilities_cashflows_list = np.array(self.liabilities_cashflows_list)
        self.assets_cashflows_list = np.array(self.assets_cashflows_list)
        return np.average(self.liabilities_cashflows_list, axis=0), np.average(self.assets_cashflows_list, axis=0)


