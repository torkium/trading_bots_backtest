import pandas as pd
from binance import ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.client import Client
from binance.enums import HistoricalKlinesType
from core.abstractstrat import AbstractStrat
from decimal import Decimal
from core.exchanges.binance import Binance
from indicators.indicators import Indicators
from core.transaction.leverageorder import LeverageOrder
from datetime import datetime


class BinanceFutures(AbstractStrat):

    feesRate = Decimal(0.1/100)
    feesRateFuture = Decimal(0.04/100)

    def __init__(self, exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame):
        super().__init__(exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame)
        self.tradingCurrency = tradingCurrency
        self.baseCurrency = baseCurrency
        self.devise = tradingCurrency+baseCurrency
        self.mainTimeFrame = mainTimeFrame

    def run(self, apiKey, apiSecret):
        self.client = Client(apiKey, apiSecret)
        self.historic = {}
        self.historic[self.mainTimeFrame] = Binance.getHistoric(self.tradingCurrency, self.baseCurrency, self.mainTimeFrame, "1 day ago UTC").tail(500)
        self.startWallet = self.wallet.getTotalAmount(self.historic[self.mainTimeFrame]['open'].iloc[0])
        self.minWallet = self.startWallet
        self.maxWallet = self.startWallet
        # open websocket
        twm = ThreadedWebsocketManager(api_key=apiKey, api_secret=apiSecret, testnet=False)
        twm.start()

        def handle_socket_message(msg):
            if msg['e'] == 'kline' and msg['s'] == self.devise:
                # https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-streams
                kline = {
                        'open': Decimal(msg['k']['o']),
                        'high': Decimal(msg['k']['h']),
                        'low': Decimal(msg['k']['l']),
                        'close': Decimal(msg['k']['c']),
                        'volume': Decimal(msg['k']['q']),
                        'close_time': Decimal(msg['k']['T']),
                        'quote_av': Decimal(msg['k']['q']),
                        'trades': Decimal(msg['k']['n']),
                        'tb_base_av': Decimal(msg['k']['V']),
                        'tb_quote_av': Decimal(msg['k']['Q']),
                        'ignore': Decimal(msg['k']['B'])
                }
                df = pd.DataFrame(kline, index=[msg['k']['t']])
                df.index = pd.to_datetime(df.index, unit='ms')

                if df.index[0] in self.historic[self.mainTimeFrame].index:
                    self.historic[self.mainTimeFrame].loc[df.index[0]] = df.iloc[0]
                    # self.historic.loc[:, df.index[0]] = df.iloc[0]
                    # self.historic._setitem_single_column(loc, v, pi)
                else:
                    self.historic[self.mainTimeFrame] = self.historic[self.mainTimeFrame].append(df)

                self.historic[self.mainTimeFrame] = self.historic[self.mainTimeFrame].tail(500)
                Indicators.setIndicators(self.historic[self.mainTimeFrame])
                # print(self.historic)
                self.runTick()

        twm.start_kline_socket(callback=handle_socket_message, symbol=self.devise, interval=self.mainTimeFrame)
        twm.join()


    def runTick(self):
         #Used to check previous period, and not current period (because not closed)
        lastIndex = self.historic[self.mainTimeFrame].index[0]
        #For each historical entry
        # for index, row in self.historic[self.mainTimeFrame].iterrows():
        row = self.historic[self.mainTimeFrame].iloc[:,-1:]
        index = self.historic[self.mainTimeFrame].index[-1]
        if self.orderInProgress == None:
            longCondition = self.longOpenConditions(lastIndex)
            shortCondition = self.shortOpenConditions(lastIndex)
            if longCondition > 0:
                #Open Long order
                amount = Decimal(self.wallet.base * longCondition / 100)
                fees =  amount * self.leverage * Decimal(self.exchange.feesRateFuture)
                self.orderInProgress = LeverageOrder(self.leverage, LeverageOrder.ORDER_TYPE_LONG, amount, fees, self.historic[self.mainTimeFrame]['open'][index], self.wallet.baseCurrency, self.wallet.tradeCurrency, index)
                self.addTransaction(self.orderInProgress, self.wallet, index)
                print(self.transactions[index])
            if longCondition == 0 and shortCondition > 0:
                #Open Short order
                amount = Decimal(self.wallet.base * shortCondition / 100)
                fees =  amount * self.leverage * Decimal(self.exchange.feesRateFuture)
                self.orderInProgress = LeverageOrder(self.leverage, LeverageOrder.ORDER_TYPE_SHORT, amount, fees, self.historic[self.mainTimeFrame]['open'][index], self.wallet.baseCurrency, self.wallet.tradeCurrency, index)
                self.addTransaction(self.orderInProgress, self.wallet, index)
                print(self.transactions[index])
        else:
            liquidateFees =  (self.orderInProgress.amount/self.orderInProgress.price * self.orderInProgress.liquidationPrice) * self.orderInProgress.leverage * Decimal(self.exchange.feesRateFuture)
            if self.orderInProgress.isLiquidated(self.historic[self.mainTimeFrame]['high'][lastIndex], self.historic[self.mainTimeFrame]['low'][lastIndex], liquidateFees):
                self.addTransaction(self.orderInProgress.liquidate(liquidateFees, index), self.wallet, index)
                self.orderInProgress = None
                print(self.transactions[index])
                print(self.wallet.toString(self.historic[self.mainTimeFrame]['open'][lastIndex]))
                lastIndex = index
                if self.wallet.base > 0:
                    print ("empty wallet")
                    return 0
                else:
                    return 0
            longCloseCondition = self.longCloseConditions(lastIndex)
            shortCloseCondition = self.shortCloseConditions(lastIndex)
            if self.orderInProgress.type == LeverageOrder.ORDER_TYPE_LONG and longCloseCondition>0:
                fees = (self.orderInProgress.amount/self.orderInProgress.price * self.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRateFuture)
                self.addTransaction(self.orderInProgress.close(fees, self.historic[self.mainTimeFrame]['open'][index], index, longCloseCondition), self.wallet, index)
                self.orderInProgress = None
                print(self.transactions[index])
                print(self.wallet.toString(self.historic[self.mainTimeFrame]['open'][index]))
                lastIndex = index
                return 0
            if self.orderInProgress.type == LeverageOrder.ORDER_TYPE_SHORT and shortCloseCondition>0:
                fees = (self.orderInProgress.amount/self.orderInProgress.price * self.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRateFuture)
                self.addTransaction(self.orderInProgress.close(fees, self.historic[self.mainTimeFrame]['open'][index], index, shortCloseCondition), self.wallet, index)
                self.orderInProgress = None
                print(self.transactions[index])
                print(self.wallet.toString(self.historic[self.mainTimeFrame]['open'][index]))
                lastIndex = index
                return 0
        lastIndex = index
        #Close the wallet at the end
        if self.orderInProgress != None:
            fees = (self.orderInProgress.amount/self.orderInProgress.price * self.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRateFuture)
            self.addTransaction(self.orderInProgress.close(fees, self.historic[self.mainTimeFrame]['open'][index], index), self.wallet, index)

        print('Date time: %s' % datetime.now())
        print(self.wallet.toString(self.historic[self.mainTimeFrame]['close'].iloc[-1]))
        print(self.getFinalLog())
