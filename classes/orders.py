from classes.transaction import Transaction
from decimal import *

class Orders:
    
    @staticmethod
    def setOrderBuy(amount, price, feesRate, time):
        to_buy = Decimal(wallet.base * percent / 100)
        fees =  to_buy * Decimal(feesRate)
        amount = Decimal(to_buy-fees) / Decimal(price)
        return Transaction(time, amount, price, "buy", fees)
    
    @staticmethod
    def setOrderSell(amount, price, feesRate, time):
        to_sell = Decimal(wallet.trade * percent / 100)
        fees =  to_sell * Decimal(feesRate)
        return Transaction(time, to_sell, price, "sell", fees * Decimal(price))
    
    @staticmethod
    def setOrderLong(amount, leverage, price, feesRate, time):
        to_long = Decimal(amount)
        fees =  to_long * leverage * Decimal(feesRate)
        to_long -= fees
        to_long = to_long / Decimal(price)
        
        iniPrice = Decimal(price) + feesRate * Decimal(price)
        tokenAmount = to_long * Decimal(leverage) / Decimal(price)
        liquidationPrice = iniPrice - (to_long/tokenAmount)
        return Transaction(time, to_long, price, "LONG", fees, leverage, liquidationPrice)
    
    @staticmethod
    def setOrderShort(amount, leverage, price, feesRate, time):
        to_short = Decimal(amount)
        fees =  to_short * leverage * Decimal(feesRate)
        to_short -= fees
        to_short = to_short / Decimal(price)
        
        iniPrice = Decimal(price) - feesRate * Decimal(price)
        tokenAmount = to_short * Decimal(leverage) / Decimal(price)
        liquidationPrice = iniPrice + (to_short/tokenAmount)
        return Transaction(time, to_short, price, "SHORT", fees, leverage, liquidationPrice)
    
    @staticmethod
    def closeLongPosition(closePrice, feesRate, transaction, time):
        closePrice = Decimal(closePrice)
        fees = Decimal(feesRate * transaction.amount * transaction.leverage * closePrice)
        return Transaction(time, transaction.amount, closePrice, "CLOSE", fees, transaction.leverage)
    
    @staticmethod
    def closeShortPosition(closePrice, feesRate, transaction, time):
        closePrice = Decimal(closePrice)
        fees = Decimal(feesRate * transaction.amount * closePrice)
        return Transaction(time, transaction.amount, closePrice, "CLOSE", fees, transaction.leverage)
    
    @staticmethod
    def liquidatePosition(transaction, feesRate, time):
        fees = feesRate * transaction.liquidationPrice
        return Transaction(time, transaction.amount, transaction.liquidationPrice, "LIQUIDATE", fees, transaction.leverage)
    
    @staticmethod
    def isLiquidated(price_high, price_low, transaction):
        if transaction.action == "LONG":
            return price_low<=transaction.liquidationPrice
        if transaction.action == "SHORT":
            return price_high>=transaction.liquidationPrice
        return False