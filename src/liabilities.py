from contract import Contract
import numpy as np


class Liabilities:
    """
    This class contains all the contracts.
    """
    def __init__(self):
        self.contracts = []

    def add_contract(self, contract: Contract):
        self.contracts.append(contract)

    def calculate_cashflows(self, market_rates):
        """
        This function calculate the accumulated cashflow of all contracts.
        Parameters
        ----------
        market_rates --- market rates of a simulation path

        Returns
        -------
        total cashflow of all contracts
        """
        accumulated_cashflows = np.zeros(len(market_rates) + 1)
        for contract in self.contracts:
            accumulated_cashflows += contract.calculate_cashflows(market_rates)
        return accumulated_cashflows

    def calculate_npvs(self, market_rates): # LEEVI DO THIS!!!!!
        """
        This function calculate the accumulated npvs of all contracts.
        Parameters
        ----------
        market_rates --- market rates of a simulation path

        Returns
        -------
        total cashflow of all contracts
        """
        accumulated_npvs = np.zeros(len(market_rates) + 1)

        for contract in self.contracts:
            accumulated_npvs += contract.calculate_cashflows(market_rates)
        return accumulated_npvs
