import numpy as np

class Swap:
    def __init__(self, maturity, face_value, received_rate, price = 1, start_time = 0):
        self.maturity = maturity
        self.face_value = face_value
        self.received_rate = received_rate
        self.price = price
        self.start_time = start_time

        self.end_time = self.start_time + self.maturity

    def set_received_rate(self, new_received_rate):
        self.received_rate = new_received_rate

  #  def calculate_payoff(self, t_end):
  #      cashflows = np.zeros(t_end + 1)
  #      received_payments = self.nominal * self.received_rate
  #      payed_payments = self.nominal * self.payed_rate
  #      net_payoff = (received_payments - payed_payments) * self.maturity
  #      cashflows[]
  #      return net_payoff
    
    def calculate_payoff(self, t_end, market_rates):
        cashflows = np.zeros(t_end + 1)
        cashflows[self.start_time] = -self.price

        market_rates_slice = market_rates[self.start_time + 1 : self.start_time + self.maturity + 1]

        cashflows[self.start_time + 1 : self.start_time + self.maturity + 1] = (
            self.face_value * self.received_rate - self.face_value * market_rates_slice
        )

        return cashflows
    
    def calculate_npv(self, spot_rates):
        cash_flows = self.calculate_payoff(self.maturity, spot_rates)
        times = np.arange(len(cash_flows))
        pvs = cash_flows / ((1 + spot_rates[self.maturity]) ** times)
        npv = np.sum(pvs[1:]) # t=0 not included
        self.price = npv # update price
        return npv