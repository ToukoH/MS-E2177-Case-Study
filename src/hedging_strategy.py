from dataclasses import dataclass

@dataclass
class HedgingStrategy:
    def __init__(self, hedging_products):
        self.hedging_products = hedging_products

    def method_for_concluding_hedging_strategy(self, policy):
        pass
