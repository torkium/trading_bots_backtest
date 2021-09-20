from binance.client import Client
import pandas as pd
from decimal import *

class Binance:
    historic = {}

    feesRate = Decimal(0.1/100)

    @staticmethod
    def getHistoric(tradingCurrency, baseCurrency, timeframe, startDate, endDate=None):
        devise = tradingCurrency+baseCurrency
        if timeframe not in Binance.historic:
            #Get history from Binance
            klinesT = Client().get_historical_klines(devise, Binance.getTimeframe(timeframe), startDate, endDate)
            for row in klinesT:
                row[1] = Decimal(row[1])
                row[2] = Decimal(row[2])
                row[3] = Decimal(row[3])
                row[4] = Decimal(row[4])
                row[5] = Decimal(row[5])
                row[7] = Decimal(row[7])
                row[9] = Decimal(row[9])
                row[10] = Decimal(row[10])
                row[11] = Decimal(row[11])
            #Set history as python DataFrame
            histo = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

            #Set the date as index
            histo = histo.set_index(histo['timestamp'])
            histo.index = pd.to_datetime(histo.index, unit='ms')
            del histo['timestamp']
            Binance.historic[timeframe] = histo
        return Binance.historic[timeframe]

    @staticmethod
    def getTimeframe(timeframe):
        if timeframe == "15m":
            return Client.KLINE_INTERVAL_15MINUTE
        if timeframe == "30m":
            return Client.KLINE_INTERVAL_30MINUTE
        if timeframe == "1h":
            return Client.KLINE_INTERVAL_1HOUR
        if timeframe == "2h":
            return Client.KLINE_INTERVAL_2HOUR
        if timeframe == "4h":
            return Client.KLINE_INTERVAL_4HOUR
        if timeframe == "12h":
            return Client.KLINE_INTERVAL_12HOUR
        if timeframe == "1d":
            return Client.KLINE_INTERVAL_1DAY
        if timeframe == "1w":
            return Client.KLINE_INTERVAL_1WEEK
        