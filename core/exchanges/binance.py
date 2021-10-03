from binance.client import Client
from binance.enums import HistoricalKlinesType
import pandas as pd
from decimal import *

class Binance:
    historic = {}

    feesRate = Decimal(0.1/100)
    feesRateFuture = Decimal(0.04/100)

    @staticmethod
    def getHistoric(tradingCurrency, baseCurrency, timeframe, startDate, endDate=None):
        devise = tradingCurrency+baseCurrency
        if timeframe not in Binance.historic:
            #Get history from Binance
            klinesT = Client().get_historical_klines(devise, Binance.getTimeframe(timeframe), startDate, endDate, klines_type=HistoricalKlinesType.FUTURES)
            Binance.historic[timeframe] = Binance.klineToDataframe(klinesT)
        return Binance.historic[timeframe]

    @staticmethod
    def getTimeframe(timeframe):
        if timeframe == "1m":
            return Client.KLINE_INTERVAL_1MINUTE
        if timeframe == "5m":
            return Client.KLINE_INTERVAL_5MINUTE
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


    @staticmethod
    def klineToDataframe(klinesT):
        for row in klinesT:
            row = Binance.normalizeLine(row)

        #Set history as python DataFrame
        histo = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

        #Set the date as index
        histo = histo.set_index(histo['timestamp'])
        histo.index = pd.to_datetime(histo.index, unit='ms')
        del histo['timestamp']

        return histo

    def normalizeLine(line):
        line[1]  = Decimal(line[1])
        line[2]  = Decimal(line[2])
        line[3]  = Decimal(line[3])
        line[4]  = Decimal(line[4])
        line[5]  = Decimal(line[5])
        line[7]  = Decimal(line[7])
        line[9]  = Decimal(line[9])
        line[10] = Decimal(line[10])
        line[11] = Decimal(line[11])

        return line