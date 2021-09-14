from classes.transaction import Transaction
from decimal import *

class Orders:
    
    @staticmethod
    def setOrderBuy(wallet, percent, price, feesRate, time):
        to_buy = (wallet.base * percent / 100) / Decimal(price)
        fees =  to_buy * Decimal(feesRate)
        wallet.trade += Decimal(to_buy - fees)
        wallet.base -= to_buy * Decimal(price)
        return Transaction(time, to_buy, price, "buy", fees*Decimal(price), wallet.baseCurrency, wallet.tradingCurrency)
    
    @staticmethod
    def setOrderSell(wallet, percent, price, feesRate, time):
        to_sell = wallet.trade * percent / 100
        fees =  to_sell * Decimal(feesRate)
        wallet.base += (to_sell - fees) * Decimal(price)
        wallet.trade -= to_sell
        return Transaction(time, to_sell, price, "sell", fees*Decimal(price), wallet.baseCurrency, wallet.tradingCurrency)