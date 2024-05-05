from contract import Contract
import numpy as np


class Liabilities:
    """
    This class contains all the contracts.
    """
    def __init__(self):
        self.contracts = []
        self.size_of_contracts = 0

    def add_contract(self, contract: Contract):
        self.contracts.append(contract)
        self.size_of_contracts += contract.size

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

    def calculate_npv(self, market_rates_rn_list, discount_rates_rn_list): 
        """
        This function calculate the accumulated npvs of all contracts.
        Parameters
        ----------
        market_rates --- market rates of a simulation path

        Returns
        -------
        total cashflow of all contracts
        """
        accumulated_npv = 0

        for contract in self.contracts:
            helper = contract.calculate_npv(market_rates_rn_list, discount_rates_rn_list)
            # print('The contract npv is: ', helper)
            accumulated_npv += helper



        return accumulated_npv
