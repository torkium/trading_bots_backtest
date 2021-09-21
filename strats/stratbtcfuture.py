from io import TextIOBase
from CsvHistory import CSVHistory
from exchanges.binance import Binance as Exchange
from classes.indicators import Indicators
from classes.wallet import Wallet
from classes.orders import Orders
import pandas as pd
import csv

class StratBtcFuture:
    historic = False
    wallet = False
    step = "main"
    baseCurrency = None
    tradingCurrency = None
    mainTimeFrame = None
    startDate = None
    endDate = None
    base = None
    trade = None
    orderInProgress = None
    leverage = None

    def __init__(self, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage, startDate, endDate=None):
        self.historic = Exchange.getHistoric(tradingCurrency, baseCurrency, mainTimeFrame, startDate, endDate)
        self.wallet = Wallet(baseCurrency, tradingCurrency, base, trade, self.historic['close'].iloc[0])
        Indicators.setIndicators(self.historic)
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency
        self.base = base
        self.trade = trade
        self.mainTimeFrame = mainTimeFrame
        self.leverage = leverage
        self.startDate = startDate
        self.endDate = endDate

    def apply(self):
        #Used to check previous period, and not current period (because not closed)
        lastIndex = self.historic.first_valid_index()
        #For each historical entry
        for index, row in self.historic.iterrows():
            if self.orderInProgress == None:
                longCondition = self.longOpenConditions(lastIndex)
                shortCondition = self.shortOpenConditions(lastIndex)
                if longCondition > 0:
                    #Open Long order
                    self.orderInProgress = Orders.setOrderLong(self.wallet.base * longCondition / 100, self.leverage, self.historic['open'][index], Exchange.feesRateFuture, index)
                    self.wallet.addTransaction(self.orderInProgress, index)
                    print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
                if longCondition == 0 and shortCondition > 0:
                    #Open Short order
                    self.orderInProgress = Orders.setOrderShort(self.wallet.base * shortCondition / 100, self.leverage, self.historic['open'][index], Exchange.feesRateFuture, index)
                    self.wallet.addTransaction(self.orderInProgress, index)
                    print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
            else:
                if Orders.isLiquidated(self.historic['high'][index], self.historic['low'][index], self.orderInProgress):
                    self.wallet.addTransaction(Orders.liquidatePosition(self.orderInProgress, Exchange.feesRateFuture, index), index)
                    self.orderInProgress = None
                    print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
                    print(self.wallet.toString())
                    lastIndex = index
                    if self.wallet.base > 0:
                        continue
                    else:
                        break
                if self.orderInProgress.action == "LONG" and self.longCloseConditions(lastIndex):
                    self.wallet.addTransaction(Orders.closeLongPosition(self.historic['open'][index], Exchange.feesRateFuture, self.orderInProgress, index), index)
                    self.orderInProgress = None
                    print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
                    print(self.wallet.toString())
                    lastIndex = index
                    continue
                if self.orderInProgress.action == "SHORT" and self.shortCloseConditions(lastIndex):
                    self.wallet.addTransaction(Orders.closeShortPosition(self.historic['open'][index], Exchange.feesRateFuture, self.orderInProgress, index), index)
                    self.orderInProgress = None
                    print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
                    print(self.wallet.toString())
                    lastIndex = index
                    continue
            lastIndex = index
        #Close the wallet at the end
        if self.orderInProgress != None:
            if self.orderInProgress.action == "LONG":
                self.wallet.addTransaction(Orders.closeLongPosition(self.historic['open'].iloc[-1], Exchange.feesRateFuture, self.orderInProgress, lastIndex), lastIndex)
            if self.orderInProgress.action == "SHORT":
                self.wallet.addTransaction(Orders.closeShortPosition(self.historic['open'].iloc[-1], Exchange.feesRateFuture, self.orderInProgress, lastIndex), lastIndex)
        self.wallet.setEnd(self.historic['close'].iloc[-1])

        print(self.wallet.toString())

        CSVHistory.write(Exchange, self.baseCurrency, self.tradingCurrency, self.mainTimeFrame, self.wallet, self.startDate, self.endDate)

    #To determine long open condition
    def longOpenConditions(self,lastIndex):
        if self.step == "main":
            if self.historic['EMA20EVOL'][lastIndex] > 1 and self.historic['EMATREND'][lastIndex] == 2 and self.historic['RSI'][lastIndex] < 70 and self.historic['RSIEVOL'][lastIndex] > 1 and self.wallet.hasPercentNotInPosition(10):
                return 50
        return 0

    #To determine long close condition
    def longCloseConditions(self, lastIndex):
        if self.step == "main":
            if (self.historic['EMA20EVOL'][lastIndex] == -1) or (self.historic['PRICEEVOL'][lastIndex] < -2 and self.historic['VOLUMEEVOL'][lastIndex] < -2):
                return True 
        return False
        
    #To determine short open condition
    def shortOpenConditions(self, lastIndex):
        if self.step == "main":
            if self.historic['EMA20EVOL'][lastIndex] < -1 and self.historic['EMATREND'][lastIndex] == -2 and self.historic['RSI'][lastIndex] > 30 and self.historic['RSIEVOL'][lastIndex] < 1 and self.wallet.hasPercentNotInPosition(10):
                return 50
        return 0
    
    #To determine short close condition
    def shortCloseConditions(self, lastIndex):
        if self.step == "main":
            if (self.historic['EMA20EVOL'][lastIndex] == 1) or (self.historic['PRICEEVOL'][lastIndex] > 1 and self.historic['VOLUMEEVOL'][lastIndex] > 1):
                return True
        return False