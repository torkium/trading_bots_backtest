from decimal import *

class Wallet:
    base = 0
    trade = 0
    start = 0
    end = 0
    trade = 0
    baseCurrency = False
    tradingCurrency = False
    transactions = {}
    totalFees = 0
    startPrice = 0
    finalPrice = False

    def __init__(self, baseCurrency, tradingCurrency, base, trade, startPrice):
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency
        self.startPrice = Decimal(startPrice)
        self.base = Decimal(base)
        self.trade = Decimal(trade)
        self.start = self.base + self.trade * self.startPrice
        self.end = self.start
    
    def setEnd(self, finalPrice):
        self.finalPrice = Decimal(finalPrice)
        self.end = self.base + self.trade * self.finalPrice

    def addTransaction(self, transaction, index):
        self.totalFees += transaction.fees
        self.transactions[index] = transaction
        self.end = self.base + self.trade*Decimal(transaction.price)
    
    def getPercentEvolution(self):
        return Decimal(100 * self.end / self.start) - Decimal(100)

    def getTotalAmount(self, price):
        return self.base + self.trade * Decimal(price)

    def toString(self):
        if self.finalPrice == False:
            return "From " + str(self.start) + " to " + str(self.end) + " " + self.baseCurrency + " (" + str(self.getPercentEvolution()) + "%) " + ". Estimated total fees : " + str(self.totalFees) + " " + self.baseCurrency + "."
        return "From " + str(self.start) + " to " + str(self.end) + " " + self.baseCurrency + " (" + str(self.getPercentEvolution()) + "%) " + ". Estimated total fees : " + str(self.totalFees) + " " + self.baseCurrency + ". ------- " + "Buy and hold result, from ", str(self.start) + " " + self.baseCurrency ," to ", str((self.start / self.startPrice) * self.finalPrice) + " " + self.baseCurrency