from dataclasses import dataclass
from liabilities import Liabilities
from hedging_product import HedgingProduct
from assets import Assets
from utils import Utils

import pandas as pd
import numpy as np
from scipy.optimize import minimize

@dataclass
class HedgingStrategy:
    def __init__(self, data, guaranteed_rate, S_liabilities):
        """
        data: Data received from Fennia, simulation data only right now
        guaranteed_rate: quaranteed rate
        """
        self.data = data
        self.guaranteed_rate = guaranteed_rate
        self.S_liabilities = S_liabilities

    def calculate_npvs(self, S_assets):
        """
        S_assets:       size of the asset position
        """

        assets = Assets(S_assets)
        liabilities = Liabilities(self.guaranteed_rate)
        
        trials = self.data['Trial'].iloc[-1]
        split_data = np.split(self.data, trials) # Data split into trials, each of which has NPV calculated

        a_npv_list = np.zeros(len(split_data))
        l_npv_list = np.zeros(len(split_data))
        
        for idx, subset in enumerate(split_data): # Loop through the split data
            market_rates    = subset['SpotRate1'] # Using forecasted spot rates as the market rates
            discount_rates  = subset['CashTotalReturnIndex']

            npv_liabilities = liabilities.npv_liabilities(market_rates, discount_rates, self.S_liabilities)
            npv_assets      = assets.npv_assets(market_rates, discount_rates)

            a_npv_list[idx] = sum(npv_assets)
            l_npv_list[idx] = sum(npv_liabilities)

        return a_npv_list, l_npv_list
    
    def calculate_means(self, a_npv_list, l_npv_list):
        """
        a_npv_list:       list of asset NPVs
        l_npv_list:       list of liability NPVs
        """

        asset_npv_mean      = np.mean(a_npv_list)
        liability_npv_mean  = np.mean(l_npv_list)

        return asset_npv_mean, liability_npv_mean

    def optimize_portfolio(self):
        res = minimize(self.portfolio_penalty())
        return res.x[0]

    def portfolio_penalty(self, s):
        a_npv_list, l_npv_list = self.calculate_npvs(s)
        penalty = - np.mean(np.minimum(a_npv_list - l_npv_list, np.zeros(a_npv_list.shape)))
        return penalty
    
    def match_means(self, S_assets):
        """
        S_assets:       size of the asset position
        """
                
        a_npv_list, l_npv_list = self.calculate_npvs(S_assets)
        asset_npv_mean, liability_npv_mean = self.calculate_means(a_npv_list, l_npv_list)
        difference = asset_npv_mean - liability_npv_mean
        print(abs(difference))
        return abs(difference)
    
    def optimize_mean_difference(self, first_guess=10000): 
        print("Optimization started.")
        # Minimize the difference between mean of assets and mean of liabilities
        x_0 = [first_guess]
        res = minimize(self.match_means, x_0, tol=0.5)
        return res.x[0] # returns the size of the asset portfolio