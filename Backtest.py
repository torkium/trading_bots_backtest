from indicators.indicators import Indicators
from strats.stratbtcfuture import StratBtcFuture
from core.exchanges.binancefutures import BinanceFutures as Exchange
from binance.client import Client
from core.userconfig import UserConfig
from operator import itemgetter


Indicators.RSI_OVERBOUGHT = 72
Indicators.RSI_OVERSOLD = 34

stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7)

#stratfuture.initBacktest("1 Aug, 2021")
#stratfuture.backtest("test.csv")



userConfig = UserConfig("userconfig.yaml")
stratfuture.run(Client, userConfig.binance_futures['api_key'], userConfig.binance_futures['api_secret'])


"""
Sample code to test multiple values for indicators
test = []
for i in range(66,76,2):
    Indicators.RSI_OVERBOUGHT = i
    for j in range(26,36,2):
        Indicators.RSI_OVERSOLD = j
        stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7)
        stratfuture.initBacktest("1 Jan, 2018")
        stratfuture.backtest()
        test.append({"param1":i, "param2":j, "fees":stratfuture.totalFees, "max_drawdown":stratfuture.maxDrawdown, "min_wallet":stratfuture.minWallet, "max_wallet":stratfuture.maxWallet, "end":stratfuture.wallet.base})

test = sorted(test, key=itemgetter('end'), reverse=True)
for row in test:
    print(row)
"""