from core.abstractstratfutures import AbstractStratFutures
from src.indicators.indicators import Indicators
from core.csvhistory import CsvHistory

class StratBtcFuture(AbstractStratFutures):

    def __init__(self, exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage):
        super().__init__(exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage)

    def setIndicators(self, timeframe):
        Indicators.RSI_OVERBOUGHT = 72
        Indicators.RSI_OVERSOLD = 34
        Indicators.setIndicators(self.exchange.historic[timeframe])

    def backtest(self, csvFileName=None):
        self.setIndicators(self.mainTimeFrame)
        super().backtest()
        if csvFileName != None:
            CsvHistory.write(csvFileName, self.exchange.historic[self.mainTimeFrame], Indicators.INDICATORS_KEYS, self.wallet, self.transactions, self.history, self.startDate, self.endDate)

    def run(self, client, apiKey, apiSecret):
        super().run(client, apiKey, apiSecret)

    def newCandleCallback(self, msg):
        super().newCandleCallback(msg)
        if self.exchange.isCandleClosed(msg):
            print("New closed Candle")
            print(msg)
            print("wait for new candle...\n")

    def longOpenConditions(self,lastIndex):
        """
        To determine long condition.
        Must return the percent of Wallet to take position.
        """
        if self.step == "main":     
            if self.exchange.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] > 1 and self.exchange.historic[self.mainTimeFrame]['EMATREND'][lastIndex] == 2 and self.exchange.historic[self.mainTimeFrame]['RSI'][lastIndex] < Indicators.RSI_OVERBOUGHT and self.exchange.historic[self.mainTimeFrame]['RSIEVOL'][lastIndex] > 1 and self.hasPercentWalletNotInPosition(10, self.wallet):
                return 50
        return 0

    #To determine long close condition
    def longCloseConditions(self, lastIndex):
        """
        To determine long close.
        Must return the percent of current long trade to close
        """
        if self.step == "main":
            if (self.exchange.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] == -1) or (self.exchange.historic[self.mainTimeFrame]['PRICEEVOL'][lastIndex] < -2 and self.exchange.historic[self.mainTimeFrame]['VOLUMEEVOL'][lastIndex] < -2):
                return 100 
            if 100*(self.exchange.historic[self.mainTimeFrame]['close'][lastIndex] - self.orderInProgress.price)/self.orderInProgress.price < -3:
                return 100
        return 0
        
    #To determine short open condition
    def shortOpenConditions(self, lastIndex):
        """
        To determine short condition.
        Must return the percent of Wallet to take position.
        """
        if self.step == "main":
            if self.exchange.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] < -1 and self.exchange.historic[self.mainTimeFrame]['EMATREND'][lastIndex] == -2 and self.exchange.historic[self.mainTimeFrame]['RSI'][lastIndex] > Indicators.RSI_OVERSOLD and self.exchange.historic[self.mainTimeFrame]['RSIEVOL'][lastIndex] < -1 and self.hasPercentWalletNotInPosition(10, self.wallet):
                return 50
        return 0
    
    #To determine short close condition
    def shortCloseConditions(self, lastIndex):
        """
        To determine short close.
        Must return the percent of current short trade to close
        """
        if self.step == "main":
            if (self.exchange.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] == 1) or (self.exchange.historic[self.mainTimeFrame]['PRICEEVOL'][lastIndex] > 1 and self.exchange.historic[self.mainTimeFrame]['VOLUMEEVOL'][lastIndex] > 1):
                return 100
        return 0
    
    def stopLossLongPrice(self, lastIndex):
        """
        To determine stop loss price for long order
        Must return the price to stop loss, or none
        """
        #return None
        stopLossPercent = 3
        return self.orderInProgress.price - self.orderInProgress.price*stopLossPercent/100
    
    def stopLossShortPrice(self, lastIndex):
        """
        To determine stop loss price for short order
        Must return the price to stop loss, or none
        """
        #return None
        stopLossPercent = 2
        return self.orderInProgress.price + self.orderInProgress.price*stopLossPercent/100