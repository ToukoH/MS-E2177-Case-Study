from Products.fixed_rate_coupon import FixedCouponBond
from Products.variable_rate_coupon import VariableCouponBond
from Products.swaption import Swaption
from Products.swap import Swap

class HedgingProduct:
    def __init__(self):
        self.products = []

    def add_fixed_coupon_bond(self, coupon=0.05, **kwargs):
        bond = FixedCouponBond(coupon, **kwargs)
        self.products.append(bond)

    def add_variable_coupon_bond(self, **kwargs):
        bond = VariableCouponBond(**kwargs)
        self.products.append(bond)

    def add_swaption(self, **kwargs):
        swaption = Swaption(**kwargs)
        self.products.append(swaption)

    def add_swap(self, **kwargs):
        swap = Swap(**kwargs)
        self.products.append(swap)

    def calculate_cash_flows(self):
        results = []
        for product in self.products:
            results.append(product.calculate_payoff())
        return results
    
    def calculate_npvs(self, spot_rates, market_rates=None):
        npvs = []
        for product in self.products:
            npv = product.calculate_npv(spot_rates)
            npvs.append(npv)
        return npvs
