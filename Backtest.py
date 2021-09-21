from strats.stratbtc import StratBtc
from strats.stratbtcfuture import StratBtcFuture

stratfuture = StratBtcFuture("USDT", "BTC", 1000, 0, "4h", 7, "1 Jan, 2018")
stratfuture.apply()