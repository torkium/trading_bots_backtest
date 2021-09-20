import ta
import pandas as pd

class Indicators:
    
    INDICATORS_KEYS = []

    @staticmethod
    def setIndicators(historic):
        periods = [20,50,100,200]
        for period in periods:
            period_string = str(period)
            historic['SMA' + period_string] = ta.trend.sma_indicator(historic['close'], period)
            historic['SMA' + period_string + 'EVOL'] = Indicators.setEvol('SMA' + period_string, historic)
            historic['EMA' + period_string] = ta.trend.ema_indicator(historic['close'], period)
            historic['EMA' + period_string + 'EVOL'] = Indicators.setEvol('EMA' + period_string, historic)
            Indicators.INDICATORS_KEYS.append('SMA' + period_string)
            Indicators.INDICATORS_KEYS.append('SMA' + period_string + 'EVOL')
            Indicators.INDICATORS_KEYS.append('EMA' + period_string)
            Indicators.INDICATORS_KEYS.append('EMA' + period_string + 'EVOL')
        historic['EMATREND'] = Indicators.setMainTrend("EMA", historic)
        historic['SMATREND'] = Indicators.setMainTrend("EMA", historic)
        historic['RSI'] = ta.momentum.RSIIndicator(historic['close'], window=14).rsi()
        historic['RSIEVOL'] = Indicators.setEvol('RSI', historic)
        historic['MACD'] = ta.trend.MACD(historic['close']).macd()
        historic['MACDDIFF'] = ta.trend.MACD(historic['close']).macd_diff()
        historic['MACDSIGN'] = ta.trend.MACD(historic['close']).macd_signal()
        Indicators.INDICATORS_KEYS.append('EMATREND')
        Indicators.INDICATORS_KEYS.append('SMATREND')
        Indicators.INDICATORS_KEYS.append('RSI')
        Indicators.INDICATORS_KEYS.append('MACD')
        Indicators.INDICATORS_KEYS.append('MACDDIFF')
        Indicators.INDICATORS_KEYS.append('MACDSIGN')
    
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