import pandas as pd
from hedging_strategy import HedgingStrategy
from hedging_product import HedgingProduct
from liabilities import Liabilities
from contract import Contract
import numpy as np
import secrets
import matplotlib.pyplot as plt


def data_processing(datapath: str) -> pd.DataFrame:
    data = pd.read_csv(datapath, delimiter=";", index_col=False)
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric)
    return data


HP = HedgingProduct()
for i in range(1, 11):
    HP.add_fixed_coupon_bond(maturity=i, coupon = 0.0) # changed from 0.05 -> 0.0
    HP.add_variable_coupon_bond(maturity=i)

L = Liabilities()
n_contracts = 100
#rng = np.random.default_rng(97584730930274884604721697427988122108)  # DO NOT CHANGE!!!
rng = np.random.default_rng(1)
maturities = rng.integers(1, 11, n_contracts)
sizes = rng.integers(1000, 50000, n_contracts)
for i in range(n_contracts):
    contract = Contract(size=sizes[i], maturity=maturities[i])
    L.add_contract(contract)


#data = data_processing("/Users/Joelv/Desktop/yliop/Fennia Case/20231231_Hf_output.csv")
data = data_processing("/Users/Joelv/Desktop/yliop/Fennia Case/Example Output EUR Swap Spot 2023Q4 updated.csv")

HS = HedgingStrategy(data, HP, L, 100)  # DO NOT MAKE  n_of_simulations big

x = HS.optimize_cashflow_difference()

print(x)

x = np.maximum(x, np.zeros(len(x)))

lc, ac = HS.calculate_optimal_average_cashflows(x)
plt.plot(lc, label='liabilities')
plt.plot(-ac, label='assets')
plt.legend()
plt.show()