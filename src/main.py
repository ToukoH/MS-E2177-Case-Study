import pandas as pd
from hedging_strategy import HedgingStrategy
from hedging_product import HedgingProduct
from liabilities import Liabilities
from contract import Contract
import numpy as np
import matplotlib.pyplot as plt
from utils import data_processing

data_path = "data/Example Output EUR Swap Spot 2023Q4 updated.csv"
data = data_processing(data_path)

n_contracts = 100
seed = np.random.default_rng(1) # or 97584730930274884604721697427988122108
coupon = 0.0

HP = HedgingProduct()
L = Liabilities()
HS = HedgingStrategy(data, HP, L, 100)

maturities = seed.integers(1, 11, n_contracts)
sizes = seed.integers(1000, 50000, n_contracts)

for i in range(1, 11):
    HP.add_fixed_coupon_bond(maturity=i, coupon = coupon)
    HP.add_variable_coupon_bond(maturity=i)

for i in range(n_contracts):
    contract = Contract(size=sizes[i], maturity=maturities[i])
    L.add_contract(contract)

x = HS.optimize_cashflow_difference()

print(x)

x = np.maximum(x, np.zeros(len(x)))

lc, ac = HS.calculate_optimal_average_cashflows(x)
plt.plot(lc, label='liabilities')
plt.plot(-ac, label='assets')
plt.legend()
plt.show()