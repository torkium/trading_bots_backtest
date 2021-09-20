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
    longAmount = 0
    shortAmount = 0
    history = {}
    last_transaction = None

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

    def addTransaction(self, transaction, index):
        self.totalFees += transaction.fees
        self.transactions[index] = transaction
        self.history[index] = {"from":{"base":self.base,"trade":self.trade},"to":{"base":self.base,"trade":self.trade}}
        if transaction.action == "buy":
            self.trade += Decimal(transaction.amount)
            self.base -= transaction.amount*transaction.price + transaction.fees
        if transaction.action == "sell":
            self.trade -= Decimal(transaction.amount)
            self.base += transaction.amount*transaction.price - transaction.fees
        if transaction.action == "LONG":
            self.base -= transaction.fees
            self.longAmount += transaction.amount
        if transaction.action == "SHORT":
            self.base -= transaction.fees
            self.shortAmount += transaction.amount
        if transaction.action == "CLOSE" or transaction.action == "LIQUIDATE":
            pr_change = transaction.price - self.last_transaction.price
            if self.last_transaction.action == "SHORT":
                pr_change *= -1
            self.base += transaction.amount*pr_change*transaction.leverage - transaction.fees
            if self.base<0:
                self.base = 0
            self.longAmount = 0
            self.shortAmount = 0
        self.history[index]['to']["base"] = self.base
        self.history[index]['to']["trade"] = self.trade
        self.last_transaction = transaction
        self.end = self.base + self.trade*Decimal(transaction.price)
    
    def getPercentEvolution(self):
        return Decimal(100 * self.end / self.start) - Decimal(100)

    def getTotalAmount(self, price):
        return self.base + self.trade * Decimal(price)

    def hasPercentBase(self, percent, price):
        return self.base >= self.getTotalAmount(price) * Decimal(percent) / 100

    def hasPercentTrade(self, percent, price):
        return self.trade * Decimal(price) >= self.getTotalAmount(price) * Decimal(percent) / 100

    def hasPercentNotInPosition(self, percent):
        return (100 - ((self.longAmount + self.shortAmount) * 100 / self.base) >= percent)

    def toString(self):
        if self.finalPrice == False:
            return "[Wallet State] : From " + str(self.start) + " to " + str(self.end) + " " + self.baseCurrency + " (" + str(self.getPercentEvolution()) + "%) " + ". Estimated total fees : " + str(self.totalFees) + " " + self.baseCurrency + "."
        return "[Wallet State] : From " + str(self.start) + " to " + str(self.end) + " " + self.baseCurrency + " (" + str(self.getPercentEvolution()) + "%) " + ". Estimated total fees : " + str(self.totalFees) + " " + self.baseCurrency + ". ------- " + "Buy and hold result, from ", str(self.start) + " " + self.baseCurrency ," to ", str(self.start * self.finalPrice / self.startPrice) + " " + self.baseCurrency