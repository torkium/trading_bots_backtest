from classes.indicators import Indicators
import pandas as pd
import csv

class CSVHistory:

    @staticmethod
    def write(exchange, baseCurrency, tradingCurrency, mainTimeFrame, wallet, startDate, endDate=None):
        historic = exchange.getHistoric(tradingCurrency, baseCurrency, mainTimeFrame, startDate, endDate)
        Indicators.setIndicators(historic)
        fileName = tradingCurrency + baseCurrency + mainTimeFrame + str(startDate) + str(endDate) + ".csv"
        fileName = fileName.replace(" ", "").replace(":","").replace("-","")
        f = open('./' + fileName, 'w', encoding='UTF8', newline="")
        writer = csv.writer(f, delimiter=';')
        headers = ['datetime', 'action', 'amount', 'fees', 'wallet_from_base', 'wallet_from_trade', 'wallet_to_base', 'wallet_to_trade', 'start_trade_amount', 'final_trade_amount', 'trade_state (%)', 'open', 'high', 'low', 'close', 'volume']
        for key in Indicators.INDICATORS_KEYS:
            headers.append(key)
        writer.writerow(headers)
        headers.remove('datetime')
        headers.remove('action')
        headers.remove('amount')
        headers.remove('fees')
        headers.remove('wallet_from_base')
        headers.remove('wallet_from_trade')
        headers.remove('wallet_to_base')
        headers.remove('wallet_to_trade')
        headers.remove('trade_state (%)')
        headers.remove('start_trade_amount')
        headers.remove('final_trade_amount')
        for index, row in historic.iterrows():
            line = []
            line.append(index)
            if wallet.transactions and index in wallet.transactions:
                line.append(str(wallet.transactions[index].action).replace(".",","))
                line.append(str(wallet.transactions[index].amount).replace(".",","))
                line.append(str(wallet.transactions[index].fees).replace(".",","))
                line.append(str(wallet.history[index]["from"]["base"]).replace(".",","))
                line.append(str(wallet.history[index]["from"]["trade"]).replace(".",","))
                line.append(str(wallet.history[index]["to"]["base"]).replace(".",","))
                line.append(str(wallet.history[index]["to"]["trade"]).replace(".",","))
                line.append(str(wallet.transactions[index].amount * wallet.transactions[index].price).replace(".",","))
                if wallet.transactions[index].finalAmount != None:
                    line.append(str(wallet.transactions[index].finalAmount).replace(".",","))
                else:
                    line.append("")
                if wallet.transactions[index].finalState != None:
                    line.append(str(wallet.transactions[index].finalState).replace(".",","))
                else:
                    line.append("")
            else:
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
                line.append("")
            for indexHeader in headers:
                line.append(str(row[indexHeader]).replace(".",","))
            writer.writerow(line)

        f.close()