from dataclasses import dataclass


@dataclass
class Liabilities:
    def __init__(self, guaranteed_rate, S = 100000):
        """
        guaranteed_rate: guaranteed_rate
        S: size of the liability position
        """
        self.guaranteed_rate = guaranteed_rate
        self.S = S

    def npv_liabilities(self, market_rates, discount_rates):
    #self.market_rates is a list of the risk free rates
    #self.guaranteed_rate is the guaranteed rate
    
        T = len(market_rates)
        cf = []
        
        #calculate the cashflows
        for t in range(T):
            r = max(market_rates.iloc[t], self.guaranteed_rate)
            
            if t<(T-1):
                cf.append(0.01*self.S) #1% probability of death
                S = 0.99*self.S*(1+r)
            else:
                cf.append(self.S)
        
        
        #calculate the discount rates if not provided
        #if discount_rates is not None:
        d = discount_rates

        """
        else:
            d = []
            for i in range(T):
                if i < 1:
                    d_i = 1
                    d.append(d_i)
                else:
                    d_i = d[i-1]/(1+self.market_rates[i-1])
                    d.append(d_i)
        """

        
        #print(d)
        #print(cf)
        cash_flows = [x * y for x, y in zip(cf, d)]
        
        return cash_flows
