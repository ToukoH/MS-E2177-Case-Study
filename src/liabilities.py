from dataclasses import dataclass

@dataclass
class Liabilities:
    def __init__(self, market_rate, guaranteed_rate, util_dependencies):
        self.market_rate = market_rate
        self.guaranteed_rate = guaranteed_rate
        self.util_dependencies = util_dependencies

    def mock_liability_method(self):
        pass
