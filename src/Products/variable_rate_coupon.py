class VariableCouponBond:
    def __init__(self, rates, F, discount_rates, S=1):
        self.rates = rates
        self.F = F
        self.discount_rates = discount_rates
        self.S = S

    def calculate_payoff(self):
        cash_flows = [(self.rates[idx] * self.F) / discount_rate for idx, discount_rate in enumerate(self.discount_rates)] + [self.F / self.discount_rates[-1]]
        return self.S * cash_flows
