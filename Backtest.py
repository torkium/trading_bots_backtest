from strats.stratbtcfuture import StratBtcFuture
from core.exchanges.binance import Binance as Exchange
from binance.client import Client
from core.userconfig import UserConfig

userConfig = UserConfig("userconfig.yaml")
stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "1m", 7)
#stratfuture.initBacktest("1 Jan, 2018")
#stratfuture.backtest()
stratfuture.run(Client, userConfig.binance_futures['api_key'], userConfig.binance_futures['api_secret'])