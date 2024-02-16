class FixedCouponBond:
    def __init__(self, coupon, F, discount_rates, S=1):
        self.coupon = coupon
        self.F = F
        self.discount_rates = discount_rates
        self.S = S

    def calculate_payoff(self):
        cash_flows = [(self.coupon * self.F) / discount_rate for discount_rate in self.discount_rates] + [self.F / self.discount_rates.iloc[-1]]
        return self.S * cash_flows
