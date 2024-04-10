import pandas as pd
from hedging_strategy import HedgingStrategy
from hedging_product import HedgingProduct
from liabilities import Liabilities
from contract import Contract
import numpy as np
import matplotlib.pyplot as plt
from utils import data_processing

data_path_real = "data/Example Output EUR Swap Spot 2023Q4 updated.csv"
data_path_rn = "data/data.csv"
data_real = data_processing(data_path_real)
data_rn = data_processing(data_path_rn)

n_contracts = 1
seed = np.random.default_rng(1) # or 97584730930274884604721697427988122108
coupon = 0.0

HP = HedgingProduct()
L = Liabilities()

maturities = seed.integers(1, 11, n_contracts)
sizes = [10000] #seed.integers(1000, 50000, n_contracts)

for i in range(1, 11):
    HP.add_fixed_coupon_bond(maturity=i, coupon = coupon)
    #HP.add_variable_coupon_bond(maturity=i)

for i in range(n_contracts):
    contract = Contract(size=sizes[i], maturity=maturities[i])
    L.add_contract(contract)

HS = HedgingStrategy(data_real, data_rn, HP, L, 100)
x = HS.optimize_cashflow_difference()

print(x)

x = np.maximum(x, np.zeros(len(x)))

time_vector = np.arange(0, 12)
bar_width = 0.35

lc, ac = HS.calculate_optimal_average_cashflows(x)
#print('The average assets cashflows are:', ac)
plt.bar(time_vector - bar_width/4, lc, bar_width/2, label='liabilities')
plt.bar(time_vector + bar_width/4, -ac, bar_width/2, label='assets')
plt.legend()
plt.show()