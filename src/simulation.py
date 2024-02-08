from dataclasses import dataclass

@dataclass
class Simulation:
    def __init__(self, hedging_products, trials, randomness_factor):
        self.hedging_products = hedging_products 
        self.trials = trials
        self.randomness_factor = randomness_factor

    def execution_method(self, insurance_period, shorter_time_frame=None):
        pass

    def select_output_format(self, format_type):
        pass

    def calculate_hedged_position(self):
        pass

    def execute_multiple_simulations(self, policy_uids):
        pass

