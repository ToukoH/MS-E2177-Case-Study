import numpy as np

class Swap:
    def __init__(self, maturity, nominal, received_rate, payed_rate):
        self.maturity = maturity
        self.nominal = nominal
        self.received_rate = received_rate
        self.payed_rate = payed_rate

    def set_received_rate(self, new_received_rate):
        self.received_rate = new_received_rate

    def set_received_rate(self, new_payed_rate):
        self.payed_rate = new_payed_rate

    def calculate_payoff(self):
        received_payments = self.nominal * self.received_rate
        payed_payments = self.nominal * self.payed_rate
        net_payoff = (received_payments - payed_payments) * self.maturity
    
        return net_payoff