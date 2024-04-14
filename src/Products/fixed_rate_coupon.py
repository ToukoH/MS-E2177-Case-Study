import numpy as np

class FixedCouponBond:
    def __init__(self, coupon, start_time=0, maturity=10, face_value=1, price=1):
        self.coupon = coupon
        self.start_time = start_time
        self.maturity = maturity
        self.face_value = face_value
        self.price = price

    def calculate_payoff(self, t_end, market_rates=None):
        cashflows = np.zeros(t_end + 1)
        cashflows[self.start_time] = - self.price
        cashflows[self.start_time + 1: self.start_time + self.maturity] = self.face_value * self.coupon
        cashflows[self.start_time + self.maturity] = self.face_value + self.face_value * self.coupon
        return cashflows
    
    def calculate_npv(self, spot_rates):
        cash_flows = self.calculate_payoff(self.maturity)
        times = np.arange(len(cash_flows))
        pvs = cash_flows / ((1 + spot_rates[self.maturity]) ** times)
        npv = np.sum(pvs[1:]) # t=0 not included
        self.price = npv # update price
        return npv
