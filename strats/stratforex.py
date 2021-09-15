from CsvHistory import CSVHistory
from exchanges.oanda import Oanda as Exchange
from classes.indicators import Indicators
from classes.wallet import Wallet
from classes.orders import Orders
import pandas as pd
import csv

class StratForex:
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
                print(self.wallet.transactions[index].toString())
            #Check sell condition
            elif sellCondition > 0:
                #Execute sell order
                self.wallet.addTransaction(Orders.setOrderSell(self.wallet, sellCondition, self.historic['open'][index], Exchange.feesRate, index), index)
                print(self.wallet.transactions[index].toString())
                print(self.wallet.toString())
            lastIndex = index
        #Close the wallet at the end
        self.wallet.setEnd(self.historic['close'].iloc[-1])

        print(self.wallet.toString())

        CSVHistory.write(Exchange, self.baseCurrency, self.tradingCurrency, self.base, self.trade, self.mainTimeFrame, self.startDate, self.endDate, self.wallet.transactions)

    #To determine buy condition
    def buyConditions(self,lastIndex):
        return 0
    
    #To determine sell condition
    def sellCondition(self, lastIndex):
        return 0