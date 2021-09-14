from classes.exchange import Exchange
from classes.indicators import Indicators
import pandas as pd
import csv

class CSVHistory:

    @staticmethod
    def write(baseCurrency, tradingCurrency, base, trade, mainTimeFrame, startDate, endDate=None, transactions=None):
        historic = Exchange.getHistoric(tradingCurrency+baseCurrency, mainTimeFrame, startDate, endDate)
        Indicators.setIndicators(historic)
        fileName = tradingCurrency + baseCurrency + mainTimeFrame + str(startDate) + str(endDate) + ".csv"
        f = open('./' + fileName, 'w', encoding='UTF8', newline="")
        writer = csv.writer(f, delimiter=';')
        headers = ['datetime', 'action', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore', 'SMA20', 'SMA50', 'SMA100', 'SMA200', 'EMA20', 'EMA50', 'EMA100', 'EMA200', 'RSI', 'MACD', 'MACDDIFF', 'MACDSIGN']
        writer.writerow(headers)
        headers.remove('datetime')
        headers.remove('action')
        for index, row in historic.iterrows():
            line = []
            line.append(index)
            if transactions and index in transactions:
                line.append(transactions[index].action)
            else:
                line.append("")
            for indexHeader in headers:
                line.append(row[indexHeader])
            writer.writerow(line)

        f.close()