import pandas as pd
import requests
import oanda_config
from datetime import datetime

class Oanda:
    historic = {}

    feesRate = 0.1/100

    session = None

    @staticmethod
    def getHistoric(tradingCurrency, baseCurrency, timeframe, startDate, endDate=None):
        if timeframe not in Oanda.historic:
            devise = tradingCurrency+ "_" + baseCurrency
            if Oanda.session == None:
                Oanda.session = requests.Session()
            url = f"{oanda_config.OANDA_URL}/instruments/{devise}/candles"
            params = {
                "price":"M",
                "from":startDate,
                "granularity":Oanda.getTimeframe(timeframe)
            }
            histo = Oanda.formatOandaResponse(Oanda.session.get(url, params=params, headers=oanda_config.SECURE_HEADER).json())
            del histo['timestamp']
            #Set values as numeric
            histo['close'] = pd.to_numeric(histo['close'])
            histo['high'] = pd.to_numeric(histo['high'])
            histo['low'] = pd.to_numeric(histo['low'])
            histo['open'] = pd.to_numeric(histo['open'])
            Oanda.historic[timeframe] = histo
        return Oanda.historic[timeframe]

    @staticmethod
    def getTimeframe(timeframe):
        if timeframe == "15m":
            return "M15"
        if timeframe == "30m":
            return "M30"
        if timeframe == "1h":
            return "H1"
        if timeframe == "2h":
            return "H2"
        if timeframe == "4h":
            return "H4"
        if timeframe == "12h":
            return "H12"
        if timeframe == "1d":
            return "D"
        if timeframe == "1w":
            return "W"
    
    @staticmethod
    def formatOandaResponse(response):
        serie_timestamp = []
        serie_open = []
        serie_high = []
        serie_low = []
        serie_close = []
        serie_volume = []
        for candle in response['candles']:
            timestamp = datetime.strptime(candle['time'].replace(".000000000Z",""), '%Y-%m-%dT%H:%M:%S')
            serie_timestamp.append(timestamp)
            serie_open.append(candle['mid']['o'])
            serie_high.append(candle['mid']['h'])
            serie_low.append(candle['mid']['l'])
            serie_close.append(candle['mid']['c'])
            serie_volume.append(candle['volume'])

        historic = pd.DataFrame()
        historic['timestamp'] = pd.Series(serie_timestamp)
        historic = historic.set_index(historic['timestamp'])
        historic['open'] = pd.Series(serie_open, index = historic.index)
        historic['high'] = pd.Series(serie_high, index = historic.index)
        historic['low'] = pd.Series(serie_low, index = historic.index)
        historic['close'] = pd.Series(serie_close, index = historic.index)
        historic['volume'] = pd.Series(serie_volume, index = historic.index)
        return historic
