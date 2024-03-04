from Products.fixed_rate_coupon import FixedCouponBond
from Products.variable_rate_coupon import VariableCouponBond
from Products.swaption import Swaption
import numpy as np


class HedgingProduct:
    def __init__(self):
        self.products = []

    def add_fixed_coupon_bond(self, coupon=0.05, F=1, S=1, discount_rates=np.zeros(60)):
        bond = FixedCouponBond(coupon, F, discount_rates, S)
        self.products.append(bond)

    def add_variable_coupon_bond(self, F=1, S=1):
        bond = VariableCouponBond(self.rates, F, self.discount_rates, S)
        self.products.append(bond)

    def add_swaption(self):
        swaption = Swaption()
        self.products.append(swaption)

    def calculate_cash_flows(self):
        results = []
        for product in self.products:
            results.append(product.calculate_payoff())
        return results
