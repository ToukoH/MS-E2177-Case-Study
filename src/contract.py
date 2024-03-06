from dataclasses import dataclass

@dataclass
class Contract:
    guaranteed_rate: float
    S: float 

    def calculate_cashflows(self, market_rates):
        T = len(market_rates)
        cf = []
        S = self.S

        for t in range(T):
            r = max(market_rates.iloc[t], self.guaranteed_rate)

            if t < (T - 1):
                cf.append(0.01 * S)  # 1% probability of death
                S = 0.99 * S * (1 + r)
            else:
                cf.append(S)

        return cf