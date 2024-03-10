from contract import Contract
import numpy as np


class Liabilities:
    def __init__(self):
        self.contracts = []

    def add_contract(self, contract: Contract):
        self.contracts.append(contract)

    def calculate_cashflows(self, market_rates):
        accumulated_cashflows = np.zeros(len(market_rates) + 1)
        for contract in self.contracts:
            accumulated_cashflows += contract.calculate_cashflows(market_rates)
        return accumulated_cashflows
