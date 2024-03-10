from contract import Contract


class Liabilities:
    def __init__(self):
        self.contracts = []

    def add_contract(self, contract: Contract):
        self.contracts.append(contract)
