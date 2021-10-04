from decimal import MAX_EMAX
import ta
import pandas as pd

class AbstractIndicators:
    
    INDICATORS_KEYS = []

    MAX_PERIOD = 400
    PERIODS = [20,50,100,200]
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    MACD_SLOW = 26
    MACD_FAST = 12
    MACD_SIGN = 9

    @staticmethod
    def setIndicators(historic):
        for period in AbstractIndicators.PERIODS:
            period_string = str(period)
            historic['SMA' + period_string] = ta.trend.sma_indicator(historic['close'], period)
            historic['SMA' + period_string + 'EVOL'] = AbstractIndicators.setEvol('SMA' + period_string, historic)
            historic['SMA' + period_string + 'SLOPE'] = AbstractIndicators.setSlope('SMA' + period_string, historic)
            historic['EMA' + period_string] = ta.trend.ema_indicator(historic['close'], period)
            historic['EMA' + period_string + 'EVOL'] = AbstractIndicators.setEvol('EMA' + period_string, historic)
            historic['EMA' + period_string + 'SLOPE'] = AbstractIndicators.setSlope('EMA' + period_string, historic)
            AbstractIndicators.INDICATORS_KEYS.append('SMA' + period_string)
            AbstractIndicators.INDICATORS_KEYS.append('SMA' + period_string + 'EVOL')
            AbstractIndicators.INDICATORS_KEYS.append('SMA' + period_string + 'SLOPE')
            AbstractIndicators.INDICATORS_KEYS.append('EMA' + period_string)
            AbstractIndicators.INDICATORS_KEYS.append('EMA' + period_string + 'EVOL')
            AbstractIndicators.INDICATORS_KEYS.append('EMA' + period_string + 'SLOPE')
        historic['EMATREND'] = AbstractIndicators.setMainTrend("EMA", historic)
        historic['SMATREND'] = AbstractIndicators.setMainTrend("EMA", historic)
        historic['RSI'] = ta.momentum.RSIIndicator(historic['close'], window=AbstractIndicators.RSI_PERIOD).rsi()
        historic['RSIEVOL'] = AbstractIndicators.setEvol('RSI', historic)
        historic['PRICEEVOL'] = AbstractIndicators.setEvol('close', historic)
        historic['VOLUMEEVOL'] = AbstractIndicators.setEvol('volume', historic)
        historic['MACD'] = ta.trend.MACD(historic['close'], window_slow=AbstractIndicators.MACD_SLOW, window_fast=AbstractIndicators.MACD_FAST, window_sign=AbstractIndicators.MACD_SIGN).macd()
        historic['MACDDIFF'] = ta.trend.MACD(historic['close']).macd_diff()
        historic['MACDSIGN'] = ta.trend.MACD(historic['close']).macd_signal()
        AbstractIndicators.INDICATORS_KEYS.append('EMATREND')
        AbstractIndicators.INDICATORS_KEYS.append('SMATREND')
        AbstractIndicators.INDICATORS_KEYS.append('RSI')
        AbstractIndicators.INDICATORS_KEYS.append('MACD')
        AbstractIndicators.INDICATORS_KEYS.append('MACDDIFF')
        AbstractIndicators.INDICATORS_KEYS.append('MACDSIGN')
    
    @staticmethod
    def setEvol(key_from, historic):
        EVOL = []
        lastIndex = None
        lastEvol = 0
        for index in historic.index:
            if lastIndex != None:
                diff = historic[key_from][index] - historic[key_from][lastIndex]
                if lastEvol>0 and diff>0:
                    lastEvol += 1
                if lastEvol<0 and diff<0:
                    lastEvol -= 1
                if lastEvol>=0 and diff<0:
                    lastEvol = -1
                if lastEvol<=0 and diff>0:
                    lastEvol = 1
            lastIndex = index
            EVOL.append(lastEvol)

        return pd.Series(EVOL, index = historic.index)
    
    @staticmethod
    def setSlope(key_from, historic):
        SLOPE = []
        lastIndex = None
        slope = 0
        for index in historic.index:
            if lastIndex != None:
                slope = 100 * (historic[key_from][index] - historic[key_from][lastIndex]) / historic[key_from][lastIndex]
            lastIndex = index
            SLOPE.append(slope)

        return pd.Series(SLOPE, index = historic.index)
    
    @staticmethod
    def setMainTrend(type, historic):
        TRENDS = []
        lastIndex = None
        for index in historic.index:
            trend = 0
            if lastIndex != None:
                if historic[type + "20"][index] >= historic[type + "50"][index] and historic[type + "50"][index] >= historic[type + "100"][index] and historic[type + "100"][index] >= historic[type + "200"][index]:
                    trend = 2
                if historic[type + "20"][index] <= historic[type + "50"][index] and historic[type + "50"][index] >= historic[type + "100"][index] and historic[type + "100"][index] >= historic[type + "200"][index]:
                    trend = 1

                if historic[type + "200"][index] >= historic[type + "100"][index] and historic[type + "100"][index] >= historic[type + "50"][index] and historic[type + "50"][index] >= historic[type + "20"][index]:
                    trend = -2
                if historic[type + "200"][index] <= historic[type + "100"][index] and historic[type + "100"][index] >= historic[type + "50"][index] and historic[type + "50"][index] >= historic[type + "20"][index]:
                    trend = -1
            lastIndex = index
            TRENDS.append(trend)

        return pd.Series(TRENDS, index = historic.index)