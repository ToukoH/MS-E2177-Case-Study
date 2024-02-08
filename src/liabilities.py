from dataclasses import dataclass


@dataclass
class Liabilities:
    def __init__(self, market_rate, guaranteed_rate, util_dependencies):
        self.market_rate = market_rate
        self.guaranteed_rate = guaranteed_rate
        self.util_dependencies = util_dependencies

    def npv_liabilities(self, discount_rates=None, S = 100000):
    #self.market_rate is a list of the risk free rates
    #self.guaranteed_rate is the guaranteed rate
    
        T = len(self.market_rate)
        cf = []
        
        #calculate the cashflows
        for t in range(T):
            r = max(self.market_rate[t], self.guaranteed_rate)
            
            if t<(T-1):
                cf.append(0.01*S) #1% probability of death
                S = 0.99*S*(1+r)
            else:
                cf.append(S)
        
        
        #calculate the discount rates if not provided
        if discount_rates is not None:
            d = discount_rates
        else:
            d = []
            for i in range(T):
                if i < 1:
                    d_i = 1
                    d.append(d_i)
                else:
                    d_i = d[i-1]/(1+self.market_rate[i-1])
                    d.append(d_i)
        
        #print(d)
        #print(cf)
        npv = [x * y for x, y in zip(cf, d)]
        
        return npv
