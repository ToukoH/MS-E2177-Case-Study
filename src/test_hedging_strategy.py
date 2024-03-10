import pandas as pd
from hedging_strategy import HedgingStrategy
from hedging_product import HedgingProduct
from liabilities import Liabilities

import matplotlib.pyplot as plt


def data_processing(datapath: str) -> pd.DataFrame:
    data = pd.read_csv(datapath, delimiter=";", index_col = False)
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric)
    return data


HP = HedgingProduct()
HP.add_fixed_coupon_bond()

data = data_processing("/Users/Joelv/Desktop/yliop/Fennia Case/20231231_Hf_output.csv")

HS = HedgingStrategy(data,0.05, HP ,10_000)

x = HS.optimize_cashflow_difference(10000)

print(x)






