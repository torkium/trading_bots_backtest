from decimal import *

class Transaction:
    time = False
    amount = False
    price = False
    action = False
    fees = False
    baseCurrency = False
    tradingCurrency = False
    leverage = False
    liquidationPrice = False

    def __init__(self, time, amount, price, action, fees, baseCurrency, tradingCurrency, leverage=1, liquidationPrice=None):
        self.time = time
        self.amount = Decimal(amount)
        self.price = Decimal(price)
        self.action = action
        self.fees = Decimal(fees)
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency
        self.leverage = Decimal(leverage)
        if liquidationPrice != None:
            self.liquidationPrice = Decimal(liquidationPrice)
        else:
            self.liquidationPrice = liquidationPrice

    def toString(self):
        return_string = "[" + str(self.time) + "][" + self.action + "][x" + str(self.leverage) + "] : " + str(self.amount) + " " + self.tradingCurrency + " at " + str(self.price) + " " + self.baseCurrency + "."
        if self.liquidationPrice:
            return_string += " Liquidation price : " + str(self.liquidationPrice) + " " + self.baseCurrency + "."
        return_string += " Estimated fees : " + str(self.fees) + " " + self.baseCurrency
        return return_string