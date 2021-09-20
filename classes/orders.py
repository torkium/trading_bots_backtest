from classes.transaction import Transaction
from decimal import *

class Orders:
    
    @staticmethod
    def setOrderBuy(wallet, percent, price, feesRate, time):
        to_buy = Decimal(wallet.base * percent / 100)
        fees =  to_buy * Decimal(feesRate)
        amount = Decimal(to_buy-fees) / Decimal(price)
        return Transaction(time, amount, price, "buy", fees, wallet.baseCurrency, wallet.tradingCurrency)
    
    @staticmethod
    def setOrderSell(wallet, percent, price, feesRate, time):
        to_sell = Decimal(wallet.trade * percent / 100)
        fees =  to_sell * Decimal(feesRate)
        return Transaction(time, to_sell, price, "sell", fees * Decimal(price), wallet.baseCurrency, wallet.tradingCurrency)
    
    @staticmethod
    def setOrderLong(wallet, percent, leverage, price, feesRate, time):
        to_long = Decimal(wallet.base * percent / 100)
        fees =  to_long * leverage * Decimal(feesRate)
        to_long -= fees
        to_long = to_long / Decimal(price)
        return Transaction(time, to_long, price, "LONG", fees, wallet.baseCurrency, wallet.tradingCurrency, leverage)
    
    @staticmethod
    def setOrderShort(wallet, percent, leverage, price, feesRate, time):
        to_short = Decimal(wallet.base * percent / 100)
        fees =  to_short * leverage * Decimal(feesRate)
        to_short -= fees
        to_short = to_short / Decimal(price)
        return Transaction(time, to_short, price, "SHORT", fees, wallet.baseCurrency, wallet.tradingCurrency, leverage)
    
    @staticmethod
    def closeLongPosition(wallet, closePrice, feesRate, transaction, time):
        closePrice = Decimal(closePrice)
        fees = Decimal(feesRate * transaction.amount * transaction.leverage * closePrice)
        return Transaction(time, transaction.amount, closePrice, "CLOSE", fees, wallet.baseCurrency, wallet.tradingCurrency, transaction.leverage)
    
    @staticmethod
    def closeShortPosition(wallet, closePrice, feesRate, transaction, time):
        closePrice = Decimal(closePrice)
        fees = Decimal(feesRate * transaction.amount * closePrice)
        return Transaction(time, transaction.amount, closePrice, "CLOSE", fees, wallet.baseCurrency, wallet.tradingCurrency, transaction.leverage)
    
    @staticmethod
    def liquidatePosition(wallet, transaction, feesRate, time):
        tokenAmount = Decimal((wallet.base * Decimal(transaction.leverage)) / Decimal(transaction.price))
        if transaction.action == "LONG":
            liquidationPrice = transaction.price + transaction.fees - Decimal(wallet.base/tokenAmount)
        if transaction.action == "SHORT":
            liquidationPrice = transaction.price - transaction.fees + Decimal(wallet.base/tokenAmount)
        fees = feesRate * liquidationPrice
        return Transaction(time, transaction.amount, liquidationPrice, "LIQUIDATE", fees, wallet.baseCurrency, wallet.tradingCurrency, transaction.leverage)
    
    @staticmethod
    def isLiquidated(wallet, price_high, price_low, transaction, feesRate):
        if transaction.action == "LONG":
            tokenAmount = Decimal((wallet.base * Decimal(transaction.leverage)) / Decimal(transaction.price))
            longLiquidationPrice = transaction.price + transaction.fees - Decimal(wallet.base/tokenAmount)
            return price_low<=longLiquidationPrice
        if transaction.action == "SHORT":
            tokenAmount = Decimal((wallet.base * Decimal(transaction.leverage)) / Decimal(transaction.price))
            longLiquidationPrice = transaction.price - transaction.fees + Decimal(wallet.base/tokenAmount)
            return price_high>=longLiquidationPrice
        return False