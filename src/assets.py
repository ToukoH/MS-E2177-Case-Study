from hedging_product import HedgingProduct
from dataclasses import dataclass
import numpy

@dataclass
class Assets:
    def __init__(self, S = 100000):
        """
        S: size of the asset position
        """
        self.S = S

    def npv_assets(self, market_rates, discount_rates):
        hedging_products = HedgingProduct(market_rates, discount_rates)

        npv = hedging_products.fixed_coupon_bond(self.S) # NPV is only one fixed coupon bond right now

        return npv
