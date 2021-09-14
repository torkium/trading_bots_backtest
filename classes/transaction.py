class Transaction:
    time = False
    amount = False
    price = False
    action = False
    fees = False
    baseCurrency = False
    tradingCurrency = False


    def __init__(self, time, amount, price, action, fees, baseCurrency, tradingCurrency):
        self.time = time
        self.amount = amount
        self.price = price
        self.action = action
        self.fees = fees
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency

    def toString(self):
        return "[" + str(self.time) + "][" + self.action + "] : " + str(self.amount) + " " + self.tradingCurrency + " at " + str(self.price) + " " + self.baseCurrency + ". Estimated fees : " + str(self.fees) + " " + self.baseCurrency