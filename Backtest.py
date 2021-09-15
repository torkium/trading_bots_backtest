from strats.stratforex import StratForex
from strats.stratbtc import StratBtc

#strat = StratForex("USD", "EUR", 1000, 0, "h4", "2018-01-01")
strat = StratBtc("USDT", "BTC", 1000, 0, "4h", "01 January 2018")
strat.apply()