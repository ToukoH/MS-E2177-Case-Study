from hedging_product import HedgingProduct
from dataclasses import dataclass

@dataclass
class Assets:
    def __init__(self, policy_holder, policy_provider, hedging_products, liabilities_dependencies):
        self.policy_holder = policy_holder
        self.policy_provider = policy_provider
        self.hedging_products = hedging_products
        self.liabilities_dependencies = liabilities_dependencies

    def method_for_concluding_hedging_strategy(self):
        pass

    def mock_assets_method(self):
        pass
