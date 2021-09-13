from classes.exchange import Exchange
from classes.indicators import Indicators
from classes.wallet import Wallet
from classes.orders import Orders
import pandas as pd

class Strat1:
    historic = False
    wallet = False
    orders = {}
    step = "main"

    def __init__(self):
        self.historic = Exchange.getHistoric("BTCUSDT", "1h", "01 January 2020")
        self.wallet = Wallet(1000,0, self.historic['close'].iloc[0])
        Indicators.setIndicators(self.historic)

    def apply(self):
        #Used to check previous period, and not current period (because not closed)
        lastIndex = self.historic.first_valid_index()

        #For each historical entry
        for index, row in self.historic.iterrows():
            #Check buy condition
            buyCondition = self.buyConditions(lastIndex)
            if buyCondition > 0:
                #Execute buy order
                Orders.setOrderBuy(self.wallet, buyCondition, self.historic['close'][index], index)
            #Check sell condition
            sellCondition = self.sellCondition(lastIndex)
            if sellCondition > 0:
                #Execute sell order
                Orders.setOrderSell(self.wallet, sellCondition, self.historic['close'][index], index)
            lastIndex = index
        #Close the wallet at the end
        self.wallet.setEnd(self.historic['close'].iloc[0], self.historic['close'].iloc[-1])

    #To determine buy condition
    def buyConditions(self,lastIndex):
        if self.step == "main":
            if self.historic['RSI'][lastIndex] < 30:
                self.step = "wait_rsi_cross_bullish"
        if self.step == "wait_rsi_cross_bullish":
            if self.historic['RSI'][lastIndex] > 30 and self.wallet.base > 10:
                return 100
            if self.historic['RSI'][lastIndex] >50:
                self.step = "main"
        return 0
    
    #To determine sell condition
    def sellCondition(self, lastIndex):
        if self.step == "main":
            if self.historic['RSI'][lastIndex] > 70:
                self.step = "wait_rsi_cross_bearish"
        if self.step == "wait_rsi_cross_bearish":
            if self.historic['RSI'][lastIndex] < 70 and self.wallet.trade > 0.0001:
                return 100
            if self.historic['RSI'][lastIndex] <50:
                self.step = "main"
        return 0