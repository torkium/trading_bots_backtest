import ta
import pandas as pd

class Indicators:
    
    @staticmethod
    def setIndicators(historic):
        historic['SMA20'] = ta.trend.sma_indicator(historic['close'], 20)
        historic['SMA50'] = ta.trend.sma_indicator(historic['close'], 50)
        historic['SMA100'] = ta.trend.sma_indicator(historic['close'], 100)
        historic['SMA200'] = ta.trend.sma_indicator(historic['close'], 200)
        historic['EMA20'] = ta.trend.ema_indicator(historic['close'], 20)
        historic['EMA50'] = ta.trend.ema_indicator(historic['close'], 50)
        historic['EMA100'] = ta.trend.ema_indicator(historic['close'], 100)
        historic['EMA200'] = ta.trend.ema_indicator(historic['close'], 200)
        historic['RSI'] = ta.momentum.RSIIndicator(historic['close'], window=14).rsi()
        historic['MACD'] = ta.trend.MACD(historic['close']).macd()
        historic['MACDDIFF'] = ta.trend.MACD(historic['close']).macd_diff()
        historic['MACDSIGN'] = ta.trend.MACD(historic['close']).macd_signal()

        EMA20EVOL = []
        lastIndex = None
        lastEma20Evol = 0
        for index in historic.index:
            if lastIndex != None:
                diff = historic['EMA20'][index] - historic['EMA20'][lastIndex]
                if lastEma20Evol>0 and diff>0:
                    lastEma20Evol += 1
                if lastEma20Evol<0 and diff<0:
                    lastEma20Evol -= 1
                if lastEma20Evol>=0 and diff<0:
                    lastEma20Evol = -1
                if lastEma20Evol<=0 and diff>0:
                    lastEma20Evol = 1
            lastIndex = index
            EMA20EVOL.append(lastEma20Evol)

        historic['EMA20EVOL'] = pd.Series(EMA20EVOL, index = historic.index)