import numpy as np

class VariableCouponBond:
    def __init__(self, start_time=0, maturity=10, face_value=1, price=1):
        self.start_time = start_time
        self.maturity = maturity
        self.face_value = face_value
        self.price = price

        self.end_time = self.start_time + self.maturity

    def calculate_payoff(self, t_end, market_rates):
        cashflows = np.zeros(t_end + 1)
        cashflows[self.start_time] = - self.price
        market_rates_slice = market_rates[self.start_time + 1: self.end_time + 1]
        cashflows[self.start_time + 1: self.end_time + 1] = self.face_value * market_rates_slice
        cashflows[self.start_time + self.maturity] += self.face_value 
        return cashflows
    
