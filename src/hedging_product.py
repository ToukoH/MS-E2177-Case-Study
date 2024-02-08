class HedgingProduct:
    
    def __init__(self, rates, discount_rates=None):
        self.rates = rates
        self.discount_rates = discount_rates

    def fixed_coupon_bond(self, coupon=0.05, F=100, S = 1):
        """
        s: amount of bonds bought
        t: time to maturity in years
        coupon: coupon
        F: face value
        """

        cash_flows = [(coupon * F) / (self.discount_rates[i]) for i in self.discount_rates] + [F/self.discount_rates[-1]]
        return S * cash_flows
    
    def variable_coupon_bond(self, F=100, S=1):
        """
        s: amount of bonds bought
        t: time to maturity in years
        coupon: coupon
        F: face value
        """

        cash_flows = [(self.rates[idx] * F) / (self.discount_rates[i]) for idx, i in enumerate(self.discount_rates)] + [F/self.discount_rates[-1]]
        return S * cash_flows

