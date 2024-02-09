from dataclasses import dataclass
from hedging_strategy import HedgingStrategy
from matplotlib import pyplot

@dataclass
class Simulation:
    def __init__(self, hedging_strategy: HedgingStrategy):
        self.hedging_strategy = hedging_strategy

    def plot_optimal_results(self):
        asset_size = self.hedging_strategy.optimize_mean_difference()
        a_npv_list, l_npv_list = self.hedging_strategy.calculate_npvs(asset_size)
        pyplot.bar(a_npv_list, alpha=0.5, label='Asset NPVs')
        pyplot.bar(l_npv_list, alpha=0.5, label='Liability NPVs')
        pyplot.legend(loc='upper right')
        pyplot.show()

