from dataclasses import dataclass

@dataclass
class Contract:
    def __init__(self, S, guaranteed_rate):
        self.S = S
        self.guaranteed_rate = guaranteed_rate

    def calculate_cashflows(self, market_rates):
        T = len(market_rates)
        cf = []
        S = self.S

        for t in range(T):
            r = max(market_rates.iloc[t], self.guaranteed_rate)

            if t < (T - 1):
                cf.append(0)  # no cashflow
                S = S * (1 + r)
            else:
                cf.append(S) # final cashflow

        return cf
