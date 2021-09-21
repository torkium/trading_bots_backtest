from decimal import *

class Transaction:
    time = False
    amount = False
    price = False
    action = False
    fees = False
    leverage = False
    liquidationPrice = False

    def __init__(self, time, amount, price, action, fees, leverage=1, liquidationPrice=None):
        self.time = time
        self.amount = Decimal(amount)
        self.price = Decimal(price)
        self.action = action
        self.fees = Decimal(fees)
        self.leverage = Decimal(leverage)
        if liquidationPrice != None:
            self.liquidationPrice = Decimal(liquidationPrice)
        else:
            self.liquidationPrice = liquidationPrice

    def toString(self, baseCurrency, tradingCurrency):
        return_string = "[" + str(self.time) + "][" + self.action + "][x" + str(self.leverage) + "] : " + str(self.amount) + " " + tradingCurrency + " at " + str(self.price) + " " + baseCurrency + "."
        if self.liquidationPrice:
            return_string += " Liquidation price : " + str(self.liquidationPrice) + " " + baseCurrency + "."
        return_string += " Estimated fees : " + str(self.fees) + " " + baseCurrency
        return return_string