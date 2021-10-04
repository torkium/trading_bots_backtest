from binance.client import Client
from binance import ThreadedWebsocketManager
from binance.enums import HistoricalKlinesType
from core.exchanges.binancespot import BinanceSpot
import pandas as pd
from decimal import *

class BinanceFutures(BinanceSpot):
    feesRate = Decimal(0.04/100)
    klines_type = HistoricalKlinesType.FUTURES