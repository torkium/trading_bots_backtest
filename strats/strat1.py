from classes.exchange import Exchange
from classes.indicators import Indicators
from classes.wallet import Wallet
from classes.orders import Orders
import pandas as pd
import csv

class Strat1:
    historic = False
    wallet = False
    step = "main"

    def __init__(self, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, startDate, endDate=None):
        self.historic = Exchange.getHistoric(tradingCurrency+baseCurrency, mainTimeFrame, startDate, endDate)
        self.wallet = Wallet(baseCurrency, tradingCurrency, base, trade, self.historic['close'].iloc[0])
        Indicators.setIndicators(self.historic)
        fileName = tradingCurrency + baseCurrency + mainTimeFrame + str(startDate) + str(endDate)
        f = open('./' + fileName, 'w')
        writer = csv.writer(f)

    def apply(self):
        #Used to check previous period, and not current period (because not closed)
        lastIndex = self.historic.first_valid_index()
        #For each historical entry
        for index, row in self.historic.iterrows():
            #Check buy condition
            buyCondition = self.buyConditions(lastIndex)
            sellCondition = self.sellCondition(lastIndex)
            if buyCondition > 0:
                #Execute buy order
                self.wallet.addTransaction(Orders.setOrderBuy(self.wallet, buyCondition, self.historic['open'][index], Exchange.feesRate, index), lastIndex)
                print(self.wallet.transactions[lastIndex].toString())
            #Check sell condition
            elif sellCondition > 0:
                #Execute sell order
                self.wallet.addTransaction(Orders.setOrderSell(self.wallet, sellCondition, self.historic['open'][index], Exchange.feesRate, index), lastIndex)
                print(self.wallet.transactions[lastIndex].toString())
                print(self.wallet.toString())
            lastIndex = index
        #Close the wallet at the end
        self.wallet.setEnd(self.historic['close'].iloc[-1])

        print(self.wallet.toString())

    #To determine buy condition
    def buyConditions(self,lastIndex):
        if self.step == "main":
            if self.historic['MACDDIFF'][lastIndex] < 0:
                self.step = "wait_macd_cross_bullish"
        if self.step == "wait_macd_cross_bullish":
            if self.historic['MACDDIFF'][lastIndex] > 0 and self.wallet.base > 10:
                self.step = "main"
                return 100
        return 0
    
    #To determine sell condition
    def sellCondition(self, lastIndex):
        if self.step == "main":
            if self.historic['MACDDIFF'][lastIndex] > 0:
                self.step = "wait_macd_cross_bearish"
        if self.step == "wait_macd_cross_bearish":
            if self.historic['MACDDIFF'][lastIndex] < 0 and self.wallet.trade > 0.0001:
                self.step = "main"
                return 100
        return 0