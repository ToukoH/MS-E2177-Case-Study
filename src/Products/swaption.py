import numpy as np

# We'll need a function to implement the execution of the swaption
# For example in hedging strategy we could just simply check if the rates go below the guaranteed rate
# and if this happens, we'll run add_swaption() in the hedging strategy class. I'm not sure if the simulation currently
# supports this kind of dynamic hedging. 

class Swaption:
    def __init__(self, notional, strike_rate, maturity, duration, premium, type):
        self.name = "Swaption"
        self.notional = notional
        self.strike_rate = strike_rate
        self.maturity = maturity
        self.duration = duration
        self.premium = premium
        self.type = type

        self.discount_rates = np.array([])
        self.forward_rates = np.array([])

    def calculate_payoff(self):
        avg_forward_rate = np.mean(self.forward_rates[:self.duration])
        if self.type == "receiver":
            value = max(self.strike_rate - avg_forward_rate, 0)
        else:
            value = max(avg_forward_rate - self.strike_rate, 0)
        
        payoff = value * self.notional * self.duration
        return payoff

    def set_discount_rates(self, discount_rates):
        self.discount_rates = np.array(discount_rates)

    def set_forward_rates(self, forward_rates):
        self.forward_rates = np.array(forward_rates)

    def calculate_npvs(self):
        annual_net_cash_flow = self.calculate_payoff()
        npvs = []
        for i in range(self.maturity):
            npv = annual_net_cash_flow / (1 + self.discount_rates[i]) ** (i + 1)
            npvs.append(npv)
        return npvs
