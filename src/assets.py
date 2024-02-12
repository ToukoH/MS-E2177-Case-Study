from hedging_product import HedgingProduct
from dataclasses import dataclass
import numpy as np

@dataclass
class Assets:
    def __init__(self, s=None):
        """
        S: size of the asset position
        """
        if s is None:
            s = np.zeros(HedgingProduct.ASSET_TYPES)
        self.s = s

    def npv_assets(self, market_rates, discount_rates):
        hedging_products = HedgingProduct(market_rates, discount_rates)

        npv = hedging_products.fixed_coupon_bond(self.S) # NPV is only one fixed coupon bond right now

        return npv
