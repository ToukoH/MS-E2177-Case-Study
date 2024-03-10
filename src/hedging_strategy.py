from dataclasses import dataclass
from liabilities import Liabilities
from hedging_product import HedgingProduct
import numpy as np
from scipy.optimize import minimize, LinearConstraint


@dataclass
class HedgingStrategy:
    def __init__(self, data, guaranteed_rate, hedging_product: HedgingProduct, liabilities: Liabilities):
        """
        data: Data received from Fennia, simulation data only right now
        guaranteed_rate: quaranteed rate
        """
        self.data = data
        self.guaranteed_rate = guaranteed_rate

        self.hp = hedging_product
        self.products = self.hp.products

        self.liabilities = liabilities
        self.contracts = self.liabilities.contracts

        self.market_rates_list = []

    def split_data(self):
        trials = self.data['Trial'].iloc[-1]
        split_data = np.split(self.data, trials)  # Data split into trials, each of which has NPV calculated

        for subset in split_data:  # Loop through the split data
            market_rates = subset['SpotRate1']  # Using forecasted spot rates as the market rates
            self.market_rates_list.append(market_rates)

    @staticmethod
    def cashflows_target_function(cashflows):
        return np.linalg.norm(cashflows)

    def match_cashflows(self, x):
        accumulated_result = 0
        for market_rates in self.market_rates_list:
            liabilities_cashflow = self.liabilities.calculate_cashflows(market_rates)
            assets_cashflow = np.multiply(x, np.array([product.calculate_payoff() for product in self.products]))
            resulting_cashflow = assets_cashflow + liabilities_cashflow
            accumulated_result += self.cashflows_target_function(resulting_cashflow)
        return accumulated_result

    def optimize_cashflow_difference(self):
        self.split_data()
        print("Optimization started.")
        x_0 = np.zeros(len(self.products))
        # constraint = LinearConstraint(A=np.identity(len(x_0)), lb=zero_time_npv, ub=zero_time_npv)
        res = minimize(self.match_cashflows, x_0, tol=0.5)
        return res.x  # returns the size of the asset portfolio


