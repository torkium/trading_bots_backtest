from src.indicators.indicators import Indicators
from src.strats.stratbtcfuture import StratBtcFuture
from core.exchanges.binancefutures import BinanceFutures as Exchange
from binance.client import Client
from core.userconfig import UserConfig
from operator import itemgetter


"""
#Sample code to launch backtest since 1 Jan, 2018
stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7)
stratfuture.initBacktest("1 Jan, 2018")
stratfuture.backtest("test.csv")
#"""

"""
#Sample code to launch strat in real mode
stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7)
userConfig = UserConfig("userconfig.yaml")
stratfuture.run(Client, userConfig.binance_futures['api_key'], userConfig.binance_futures['api_secret'])
#"""

"""
#Sample code to test multiple values for indicators
test = []
for i in range(60,80,2):
    Indicators.RSI_OVERBOUGHT = i
    for j in range(20,40,2):
        Indicators.RSI_OVERSOLD = j
        stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7)
        stratfuture.initBacktest("1 Jan, 2018")
        stratfuture.backtest()
        test.append({"param1":i, "param2":j, "fees":stratfuture.totalFees, "max_drawdown":stratfuture.maxDrawdown, "min_wallet":stratfuture.minWallet, "max_wallet":stratfuture.maxWallet, "end":stratfuture.wallet.base})

test = sorted(test, key=itemgetter('end'), reverse=True)
for row in test:
    print(row)
#"""

"""
#Sample code to test multiple leverage
test = []
for i in range(1,35,1):
    stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", i)
    stratfuture.initBacktest("1 Jan, 2018")
    stratfuture.backtest()
    test.append({"leverage":i, "fees":stratfuture.totalFees, "max_drawdown":stratfuture.maxDrawdown, "min_wallet":stratfuture.minWallet, "max_wallet":stratfuture.maxWallet, "end":stratfuture.wallet.base})

test = sorted(test, key=itemgetter('end'), reverse=True)
for row in test:
    print(row)
#"""