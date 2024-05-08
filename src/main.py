import pandas as pd
from hedging_strategy import HedgingStrategy
from hedging_product import HedgingProduct
from liabilities import Liabilities
from contract import Contract
import numpy as np
import matplotlib.pyplot as plt
from utils import data_processing

### variables
shock = 150 # -150, -100, -50, 50, 100, 150
opt_type = 1 # 1: min dot product, 2: min 5th percentile, 3: min biggest loss
guar_rate = 0.035 # 0.02, 0.035, 0.06
###

data_path_real = "data/Example Output EUR Swap Spot 2023Q4 updated.csv"
data_path_rn = "data/data.csv"

if shock == -150:
    data_path_rn = "data/20231231_Hf_output_minus150.csv"
elif shock == -100:
    data_path_rn = "data/20231231_Hf_output_minus100.csv"
elif shock == -50:
    data_path_rn = "data/20231231_Hf_output_minus50.csv"
elif shock == 50:
    data_path_rn = "data/20231231_Hf_output_plus50.csv"
elif shock == 100:
    data_path_rn = "data/20231231_Hf_output_plus100.csv"
elif shock == 150:
    data_path_rn = "data/20231231_Hf_output_plus150.csv"

data_real = data_processing(data_path_real)
data_rn = data_processing(data_path_rn)

n_contracts = 50
seed = np.random.default_rng(97584730930274884604721697427988122108) # or 97584730930274884604721697427988122108
coupon = 0.0

HP = HedgingProduct()
L = Liabilities()

maturities = seed.integers(1, 11, n_contracts)
sizes = seed.integers(1000, 50000, n_contracts)

for i in range(1, 11):
    HP.add_fixed_coupon_bond(maturity=i, coupon = coupon)
    HP.add_swap(maturity = i, face_value = 1, received_rate = guar_rate)
    HP.add_variable_coupon_bond(maturity=i)


for i in range(n_contracts):
    contract = Contract(size=sizes[i], maturity=maturities[i], guaranteed_rate=guar_rate)
    L.add_contract(contract)

"""
contract = Contract(size=10_000, maturity=10)
L.add_contract(contract)
"""

HS = HedgingStrategy(data_real, data_rn, HP, L, opt_type, 100)
x = HS.optimize_cashflow_difference()

print(x)

x = np.maximum(x, np.zeros(len(x)))

products_df = pd.DataFrame(columns=['Product', 'Maturity', 'Price', 'Position size'])

for idx, i in enumerate(HP.products):
    products_df.loc[idx] = [i.name, i.maturity, i.price, x[idx]]

time_vector = np.arange(0, 12)
bar_width = 0.35

lc, ac = HS.calculate_optimal_average_cashflows(x)

acl_removed = np.array([inner_list[1:] for inner_list in HS.assets_cashflows_list])
lcl_removed = np.array([inner_list[1:] for inner_list in HS.liabilities_cashflows_list])

simulation_cashflows = np.sum((acl_removed + lcl_removed), axis=1)
#simulation_cashflows = np.sum((HS.assets_cashflows_list + HS.liabilities_cashflows_list), axis=1)
print(f"Mean of total cashflows: {np.mean(simulation_cashflows)}")
print(f"Standard deviation of cashflows: {np.std(simulation_cashflows)}")
print(f"5-percentile of cashflows: {np.percentile(simulation_cashflows, 5)}")

# Plot 1
fig1 = plt.figure(1)
plt.hist(simulation_cashflows, bins=50)
plt.axvline(x = 0, color = 'b', label = 'axvline - full height')
fig1.show()

# Plot 2
fig2 = plt.figure(2)
plt.bar(time_vector - bar_width/4, lc, bar_width/2, label='liabilities')
plt.bar(time_vector + bar_width/4, -ac, bar_width/2, label='assets')
plt.legend()
fig2.show()

# Plot 3
ax1 = products_df.groupby(['Maturity', 'Product'])['Position size'].sum().unstack().plot.bar(stacked=True)
fig3 = ax1.get_figure()
fig3.show()

"""
# Plot 4
ax2 = products_df.groupby(['Product'])['Position size'].sum().plot.pie()
fig4 = ax2.get_figure()
fig4.show()
"""
input() # Shows all figures