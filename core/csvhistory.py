import pandas as pd
import csv

class CsvHistory:

    @staticmethod
    def write(csvFileName, historic, indicators_keys, wallet, transactions, history, startDate, endDate=None):
        f = open('./' + csvFileName, 'w', encoding='UTF8', newline="")
        writer = csv.writer(f, delimiter=';')
        headers = ['datetime', 'action', 'amount', 'fees', 'wallet_from_base', 'wallet_from_trade', 'wallet_to_base', 'wallet_to_trade', 'start_trade_amount', 'final_trade_amount', 'trade_state (%)', 'drawdown (%)', 'open', 'high', 'low', 'close', 'volume']
        for key in indicators_keys:
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
        headers.remove('drawdown (%)')
        for index, row in historic.iterrows():
            line = []
            line.append(index)
            if transactions and index in transactions:
                line.append(str(transactions[index].type).replace(".",","))
                line.append(str(transactions[index].amount).replace(".",","))
                line.append(str(transactions[index].fees).replace(".",","))
                line.append(str(history[index]["from"]["base"]).replace(".",","))
                line.append(str(history[index]["from"]["trade"]).replace(".",","))
                line.append(str(history[index]["to"]["base"]).replace(".",","))
                line.append(str(history[index]["to"]["trade"]).replace(".",","))
                line.append(str(transactions[index].amount).replace(".",","))
                if transactions[index].finalAmount != None:
                    line.append(str(transactions[index].finalAmount).replace(".",","))
                    line.append(str(transactions[index].percentGain).replace(".",","))
                else:
                    line.append("")
                    line.append("")
                line.append(str(history[index]["drawdown"]).replace(".",","))
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
                line.append("")
            for indexHeader in headers:
                line.append(str(row[indexHeader]).replace(".",","))
            writer.writerow(line)

        f.close()