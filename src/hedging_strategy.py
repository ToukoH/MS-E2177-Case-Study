from dataclasses import dataclass
from liabilities import Liabilities
from hedging_product import HedgingProduct
from assets import Assets
from utils import Utils
import pandas as pd
import numpy as np
from scipy.optimize import minimize, LinearConstraint


@dataclass
class HedgingStrategy:
    def __init__(self, data, guaranteed_rate, hedging_product: HedgingProduct, S_liabilities):
        """
        data: Data received from Fennia, simulation data only right now
        guaranteed_rate: quaranteed rate
        """
        self.data = data
        self.guaranteed_rate = guaranteed_rate
        self.S_liabilities = S_liabilities
        self.hp = hedging_product
        self.products = self.hp.products
        self.market_rates_list = []

    def split_data(self):
        trials = self.data['Trial'].iloc[-1]
        split_data = np.split(self.data, trials)  # Data split into trials, each of which has NPV calculated

        for subset in split_data:  # Loop through the split data
            market_rates = subset['SpotRate1']  # Using forecasted spot rates as the market rates
            self.market_rates_list.append(market_rates)

    def match_cashflows(self, x):
        # Need to know the liabilities cashflow!!!
        accumulated_result = 0
        for market_rates in self.market_rates_list:
            l = Liabilities(self.guaranteed_rate)
            liabilities_cashflow = l.calculate_cashflows(market_rates, self.S_liabilities)
            assets_cashflow = np.multiply(x, np.array([product.calculate_payoff() for product in self.products]))
            accumulated_result += np.linalg.norm(assets_cashflow - liabilities_cashflow)
        return accumulated_result

    def optimize_cashflow_difference(self, zero_time_npv):
        self.split_data()
        print("Optimization started.")
        x_0 = np.zeros(len(self.products))
        x_0 += zero_time_npv/len(x_0)
        constraint = LinearConstraint(A=np.identity(len(x_0)), lb=zero_time_npv, ub=zero_time_npv)
        res = minimize(self.match_cashflows, x_0, tol=0.5)
        return res.x  # returns the size of the asset portfolio

# BELOW NOT IN USE


def calculate_npvs(self, S_assets):
    """
    S_assets:       size of the asset position
    """

    assets = Assets(S_assets)
    liabilities = Liabilities(self.guaranteed_rate)

    trials = self.data['Trial'].iloc[-1]
    split_data = np.split(self.data, trials)  # Data split into trials, each of which has NPV calculated

    a_npv_list = []
    l_npv_list = []

    for subset in split_data:  # Loop through the split data
        market_rates = subset['SpotRate1']  # Using forecasted spot rates as the market rates
        discount_rates = subset['CashTotalReturnIndex']

        npv_liabilities = liabilities.npv_liabilities(market_rates, discount_rates, self.S_liabilities)
        npv_assets = assets.npv_assets(market_rates, discount_rates)

        a_npv_list.append(sum(npv_assets))
        l_npv_list.append(sum(npv_liabilities))

    return a_npv_list, l_npv_list


def calculate_means(self, a_npv_list, l_npv_list):
    """
    a_npv_list:       list of asset NPVs
    l_npv_list:       list of liability NPVs
    """

    asset_npv_mean = sum(a_npv_list) / len(a_npv_list)
    liability_npv_mean = sum(l_npv_list) / len(l_npv_list)

    return asset_npv_mean, liability_npv_mean


def match_means(self, S_assets):
    """
    S_assets:       size of the asset position
    """

    a_npv_list, l_npv_list = self.calculate_npvs(S_assets)
    asset_npv_mean, liability_npv_mean = self.calculate_means(a_npv_list, l_npv_list)
    difference = asset_npv_mean - liability_npv_mean
    print(abs(difference))
    return abs(difference)
