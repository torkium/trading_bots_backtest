import ta

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