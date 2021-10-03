from strats.stratbtcfuture import StratBtcFuture
from core.exchanges.binance import Binance as Exchange
from core.userconfig import UserConfig

"""
load user configuration
"""
userConfig = UserConfig()

stratfuture = StratBtcFuture(Exchange, "USDT", "BTC", 100, 0, "1m", 3)
stratfuture.run(userConfig.binance_futures['api_key'], userConfig.binance_futures['api_secret'])
# stratfuture.demo(userConfig.binance_futures['api_key'], userConfig.binance_futures['api_secret'])
