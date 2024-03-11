from dataclasses import dataclass

import numpy as np


@dataclass
class Contract:
    def __init__(self, size, guaranteed_rate=0.035, start_time=0, maturity=10):
        self.size = size
        self.guaranteed_rate = guaranteed_rate
        self.start_time = start_time
        self.maturity = maturity

    def __repr__(self):
        return f"Contract(size={self.size}, maturity={self.maturity})"

    def calculate_cashflows(self, market_rates):
        """
        This function calculates cashflows with respect to the market rates and the guaranteed rate.
        Cashflows are calculated with respect to Fennia, so the cashflow at t = start_time is positive
        and at t = start_time + maturity is negative.
        Parameters
        ----------
        market_rates --- market rates for the whole simulated period [1, t_end]. For a correct answer
        [len(market_rates) >= start_time + maturity] should hold which is an indicator that the contract
        ends inside the considered period of the simulation.

        Returns
        -------
        An array of cashflows for the whole simulated period. It would have two non-zero values.
        len(cashflows) = len(market_rates) + 1, because cashflows are returned for t in [0, t_end]

        """
        cashflows = np.zeros(len(market_rates) + 1)

        market_rates_slice = market_rates[self.start_time + 1: self.start_time + self.maturity + 1]
        guaranteed_rates_slice = np.array([self.guaranteed_rate] * self.maturity)
        applied_rates = np.maximum(market_rates_slice, guaranteed_rates_slice)
        total_multiplier = np.prod(applied_rates + 1)

        cashflows[self.start_time] = self.size
        cashflows[self.start_time + self.maturity] = - self.size * total_multiplier

        return cashflows
