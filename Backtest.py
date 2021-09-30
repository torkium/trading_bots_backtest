from strats.stratbtcfuture import StratBtcFuture
from core.exchanges.binance import Binance as Exchange

stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 1000, 0, "4h", 7, "1 Jan, 2018")
stratfuture.apply()