from CsvHistory import CSVHistory
from exchanges.binance import Binance as Exchange
from classes.indicators import Indicators
from classes.wallet import Wallet
from classes.orders import Orders
import pandas as pd
import csv

class StratBtc:
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

    def __init__(self, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, startDate, endDate=None):
        self.historic = Exchange.getHistoric(tradingCurrency, baseCurrency, mainTimeFrame, startDate, endDate)
        self.wallet = Wallet(baseCurrency, tradingCurrency, base, trade, self.historic['close'].iloc[0])
        Indicators.setIndicators(self.historic)
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency
        self.base = base
        self.trade = trade
        self.mainTimeFrame = mainTimeFrame
        self.startDate = startDate
        self.endDate = endDate

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
                self.wallet.addTransaction(Orders.setOrderBuy(self.wallet, buyCondition, self.historic['open'][index], Exchange.feesRate, index), index)
                print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
            #Check sell condition
            elif sellCondition > 0:
                #Execute sell order
                self.wallet.addTransaction(Orders.setOrderSell(self.wallet, sellCondition, self.historic['open'][index], Exchange.feesRate, index), index)
                print(self.wallet.transactions[index].toString(self.wallet.baseCurrency, self.wallet.tradingCurrency))
                print(self.wallet.toString())
            lastIndex = index
        #Close the wallet at the end
        
        if self.wallet.trade != 0:
            self.wallet.addTransaction(Orders.setOrderSell(self.wallet, 100, self.historic['open'][index], Exchange.feesRate, index), index)
        self.wallet.setEnd(self.historic['close'].iloc[-1])


        self.wallet.setEnd(self.historic['close'].iloc[-1])

        print(self.wallet.toString())

        CSVHistory.write(Exchange, self.baseCurrency, self.tradingCurrency, self.mainTimeFrame, self.wallet, self.startDate, self.endDate)

    #To determine buy condition
    def buyConditions(self,lastIndex):
        if self.step == "main":
            if self.historic['EMA20EVOL'][lastIndex] > 1 and self.wallet.hasPercentBase(10, self.historic['close'][lastIndex]):
                return 100
        return 0
    
    #To determine sell condition
    def sellCondition(self, lastIndex):
        if self.step == "main":
            if (self.historic['EMA20EVOL'][lastIndex] == -2 or (self.historic['EMA20EVOL'][lastIndex] >= 1 and self.historic['RSI'][lastIndex] > 80)) and self.wallet.hasPercentTrade(10, self.historic['close'][lastIndex]):
                return 100
        return 0