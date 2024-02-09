from dataclasses import dataclass
from hedging_strategy import HedgingStrategy
from matplotlib import pyplot
import numpy as np

@dataclass
class Simulation:
    def __init__(self, hedging_strategy: HedgingStrategy):
        self.hedging_strategy = hedging_strategy

    def plot_optimal_results(self):
        asset_size = self.hedging_strategy.optimize_mean_difference()
        print(f"Optimal asset size is: {asset_size}")
        a_npv_list, l_npv_list = self.hedging_strategy.calculate_npvs(asset_size)
        print("NPVs calculated.")
        #subtracted_npv = np.subtract(a_npv_list, l_npv_list)
        min_npv = min(a_npv_list + l_npv_list)
        max_npv = max(a_npv_list + l_npv_list)

        print(f"Minimum NPV: {min_npv}")
        print(f"Maximum NPV: {max_npv}")

        #bins = np.linspace(min(subtracted_npv), max(subtracted_npv), 1000)
        bins = np.linspace(min_npv, max_npv, 1000)
        pyplot.hist(a_npv_list, bins, alpha=0.5, label='Asset - Liability NPVs')
        pyplot.hist(l_npv_list, bins, alpha=0.5, label='Liability NPVs')
        pyplot.legend(loc='upper right')
        pyplot.show()

