from contract import Contract

class Liabilities:
    def __init__(self):
        self.contracts = []

    def add_contract(self, contract: Contract):
        self.contracts.append(contract)

    def npv_liabilities(self, market_rates, discount_rates):
        T = len(market_rates)
        aggregate_cf = [0] * T

        for contract in self.contracts:
            cf = contract.calculate_cashflows(market_rates)
            
            for i in range(T):
                aggregate_cf[i] += cf[i]

        discounted_cf = [cf * d for cf, d in zip(aggregate_cf, discount_rates)]

        return discounted_cf
