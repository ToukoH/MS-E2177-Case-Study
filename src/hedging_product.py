class HedgingProduct:

    def __init__(self, rates, discount_rates):
        self.rates = rates
        self.discount_rates = discount_rates


class FixedCouponBond(HedgingProduct):
    def __init__(self, coupon, *args, **kwargs):
        self.coupon = coupon
        super().__init__(*args, **kwargs)

    def calculate_payoff(self, F=100, S = 1):
        """
        s: amount of bonds bought
        t: time to maturity in years
        coupon: coupon
        F: face value
        """
        coupon = self.coupon

        cash_flows = [(coupon * F) / (discount_rate) for discount_rate in self.discount_rates] + [F/self.discount_rates.iloc[-1]]
        return S * cash_flows


class VariableCouponBond(HedgingProduct):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def calculate_payoff(self, F=100, S=1):
        """
        s: amount of bonds bought
        t: time to maturity in years
        coupon: coupon
        F: face value
        """

        cash_flows = [(self.rates[idx] * F) / (discount_rate) for idx, discount_rate in enumerate(self.discount_rates)] + [F/self.discount_rates[-1]]
        return S * cash_flows



