from hedging_strategy import HedgingStrategy
from simulation import Simulation
from hedging_product import HedgingProduct

import pandas as pd

def data_processing(datapath: str) -> pd.DataFrame:
    data = pd.read_csv(datapath, delimiter=";", index_col = False)
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric)
    #print(data.index)
    return data

def main():
    data = data_processing("C:/Users/Vlad/Desktop/OR Case Study/MS-E2177-Case-Study/data/20231231_Hf_output.csv")

    HP = HedgingProduct()
    HP.add_fixed_coupon_bond()

    hedging_strategy = HedgingStrategy(data,
                                       0.05,
                                       HP,
                                       10_000)

    simulation = Simulation(hedging_strategy)
    simulation.plot_optimal_results()

if __name__ == '__main__':
    main()