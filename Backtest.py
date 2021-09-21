from strats.stratforex import StratForex
from strats.stratbtc import StratBtc
from strats.stratbtcfuture import StratBtcFuture

#stratforex = StratForex("USD", "EUR", 1000, 0, "1h", 100, "2020-09-01")
#stratforex.apply()
stratfuture = StratBtcFuture("USDT", "BTC", 1000, 0, "4h", 7, "1 Jan, 2018")
stratfuture.apply()