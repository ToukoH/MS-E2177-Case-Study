import numpy as np

class Swaption:
    def __init__(self, notional, strike_rate, maturity, underlying_swap_years):
        self.notional = notional
        self.strike_rate = strike_rate
        self.maturity = maturity
        self.underlying_swap_years = underlying_swap_years
        self.discount_rates = np.array([])
        self.forward_rates = np.array([])

    def calculate_payoff(self):
        """
        Calculate the payoff of the swaption at expiration.
        """
        avg_forward_rate = np.mean(self.forward_rates[:self.underlying_swap_years])
        value = max(avg_forward_rate - self.strike_rate, 0)
        payoff = value * self.notional * self.underlying_swap_years
        return payoff

    def set_discount_rates(self, discount_rates):
        self.discount_rates = np.array(discount_rates)

    def set_forward_rates(self, forward_rates):
        self.forward_rates = np.array(forward_rates)
