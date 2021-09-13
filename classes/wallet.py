class Wallet:
    base = 0
    trade = 0
    start = 0
    end = 0
    trade = 0

    def __init__(self, base, trade, startPrice):
        self.base = base
        self.trade = trade
        self.start = self.base + self.trade * startPrice
    
    def setEnd(self, startPrice, finalPrice):
        self.end = self.base + self.trade * finalPrice
        print("Final result, from",self.start,' to ', self.end ,'USDT')
        print("Buy and hold result, from ", self.start ," to ", (self.start / startPrice) * finalPrice,'USDT')