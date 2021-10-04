from core.abstractstrat import AbstractStrat
from core.transaction.leverageorder import LeverageOrder
from decimal import *

class AbstractStratFutures(AbstractStrat):
    leverage = None
    orderInProgress = None
    walletInPosition = None

    def __init__(self, exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage):
        super().__init__(exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame)
        self.leverage = leverage
        self.walletInPosition = 0

    def backtest(self, csvFileName=None):
        #Used to check previous period, and not current period (because not closed)
        lastIndex = self.exchange.historic[self.mainTimeFrame].first_valid_index()
        #For each historical entry
        for index, row in self.exchange.historic[self.mainTimeFrame].iterrows():
            if self.orderInProgress == None:
                longCondition = self.longOpenConditions(lastIndex)
                shortCondition = self.shortOpenConditions(lastIndex)
                if longCondition > 0:
                    #Open Long order
                    amount = Decimal(self.wallet.base * longCondition / 100)
                    fees =  amount * self.leverage * Decimal(self.exchange.feesRate)
                    self.orderInProgress = LeverageOrder(self.leverage, LeverageOrder.ORDER_TYPE_LONG, amount, fees, self.exchange.historic[self.mainTimeFrame]['open'][index], self.wallet.baseCurrency, self.wallet.tradeCurrency, index)
                    self.addTransaction(self.orderInProgress, self.wallet, index)
                    print(self.transactions[index])
                if longCondition == 0 and shortCondition > 0:
                    #Open Short order
                    amount = Decimal(self.wallet.base * shortCondition / 100)
                    fees =  amount * self.leverage * Decimal(self.exchange.feesRate)
                    self.orderInProgress = LeverageOrder(self.leverage, LeverageOrder.ORDER_TYPE_SHORT, amount, fees, self.exchange.historic[self.mainTimeFrame]['open'][index], self.wallet.baseCurrency, self.wallet.tradeCurrency, index)
                    self.addTransaction(self.orderInProgress, self.wallet, index)
                    print(self.transactions[index])
            else:
                liquidateFees =  (self.orderInProgress.amount/self.orderInProgress.price * self.orderInProgress.liquidationPrice) * self.orderInProgress.leverage * Decimal(self.exchange.feesRate)
                if self.orderInProgress.isLiquidated(self.exchange.historic[self.mainTimeFrame]['high'][lastIndex], self.exchange.historic[self.mainTimeFrame]['low'][lastIndex], liquidateFees):
                    self.addTransaction(self.orderInProgress.liquidate(liquidateFees, index), self.wallet, index)
                    self.orderInProgress = None
                    print(self.transactions[index])
                    print(self.wallet.toString(self.exchange.historic[self.mainTimeFrame]['open'][lastIndex]))
                    lastIndex = index
                    if self.wallet.base > 0:
                        continue
                    else:
                        break
                longCloseCondition = self.longCloseConditions(lastIndex)
                shortCloseCondition = self.shortCloseConditions(lastIndex)
                if self.orderInProgress.type == LeverageOrder.ORDER_TYPE_LONG and longCloseCondition>0:
                    fees = (self.orderInProgress.amount/self.orderInProgress.price * self.exchange.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRate)
                    self.addTransaction(self.orderInProgress.close(fees, self.exchange.historic[self.mainTimeFrame]['open'][index], index, longCloseCondition), self.wallet, index)
                    self.orderInProgress = None
                    print(self.transactions[index])
                    print(self.wallet.toString(self.exchange.historic[self.mainTimeFrame]['open'][index]))
                    lastIndex = index
                    continue
                if self.orderInProgress.type == LeverageOrder.ORDER_TYPE_SHORT and shortCloseCondition>0:
                    fees = (self.orderInProgress.amount/self.orderInProgress.price * self.exchange.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRate)
                    self.addTransaction(self.orderInProgress.close(fees, self.exchange.historic[self.mainTimeFrame]['open'][index], index, shortCloseCondition), self.wallet, index)
                    self.orderInProgress = None
                    print(self.transactions[index])
                    print(self.wallet.toString(self.exchange.historic[self.mainTimeFrame]['open'][index]))
                    lastIndex = index
                    continue
            lastIndex = index
        #Close the wallet at the end
        if self.orderInProgress != None:
            fees = (self.orderInProgress.amount/self.orderInProgress.price * self.exchange.historic[self.mainTimeFrame]['open'][index]) * self.orderInProgress.leverage * Decimal(self.exchange.feesRate)
            self.addTransaction(self.orderInProgress.close(fees, self.exchange.historic[self.mainTimeFrame]['open'][index], index), self.wallet, index)

        print(self.wallet.toString(self.exchange.historic[self.mainTimeFrame]['close'].iloc[-1]))
        print(self.getFinalLog())

    

    def addTransaction(self, transaction, wallet, index):
        self.totalFees += transaction.fees
        self.history[index] = {"from":{"base":wallet.base,"trade":wallet.trade},"to":{"base":wallet.base,"trade":wallet.trade}, "drawdown": 0}
        if transaction.type == LeverageOrder.ORDER_TYPE_LONG:
            wallet.base -= transaction.fees
            self.walletInPosition += transaction.amount
        if transaction.type == LeverageOrder.ORDER_TYPE_SHORT:
            wallet.base -= transaction.fees
            self.walletInPosition += transaction.amount
        if transaction.type == LeverageOrder.ORDER_TYPE_CLOSE:
            pr_change = transaction.price - self.last_transaction.price
            if self.last_transaction.type == LeverageOrder.ORDER_TYPE_SHORT:
                pr_change *= -1
            gain = transaction.amount*(pr_change/self.last_transaction.price)*transaction.leverage - transaction.fees
            transaction.finalAmount = transaction.amount + gain 
            wallet.base += gain
            self.walletInPosition -= transaction.amount
        if transaction.type == LeverageOrder.ORDER_TYPE_LIQUIDATE:
            wallet.base -= self.last_transaction.amount
            self.walletInPosition = 0
        self.transactions[index] = transaction
        self.history[index]['to']["base"] = wallet.base
        self.history[index]['to']["trade"] = wallet.trade
        self.last_transaction = transaction
        wallet_total_amount = wallet.getTotalAmount(Decimal(transaction.price))
        if wallet_total_amount > self.maxWallet:
            self.maxWallet = wallet_total_amount
            self.currentDrawdown = 0
        if wallet_total_amount < self.minWallet:
            self.minWallet = wallet_total_amount
        if wallet_total_amount < self.maxWallet:
            self.currentDrawdown = 100 * (self.maxWallet - wallet_total_amount) / self.maxWallet
            self.history[index]["drawdown"] = self.currentDrawdown
            if self.currentDrawdown > self.maxDrawdown:
                self.maxDrawdown = self.currentDrawdown

        
    def getPercentWalletInPosition(self, wallet):
        if self.walletInPosition == None or wallet.base == None or wallet.base == 0:
            return 0
        return Decimal(self.walletInPosition/wallet.base)*100
    
    def hasPercentWalletNotInPosition(self, percent, wallet):
        if wallet.base == None:
            return False
        return 100-self.getPercentWalletInPosition(wallet)>=percent

    #To determine long open condition
    def longOpenConditions(self,lastIndex):
        """
        To determine long condition.
        Must return the percent of Wallet to take position.
        """
        return 0

    #To determine long close condition
    def longCloseConditions(self, lastIndex):
        """
        To determine long close.
        Must return the percent of current long trade to close
        """
        return 100
        
    #To determine short open condition
    def shortOpenConditions(self, lastIndex):
        """
        To determine short condition.
        Must return the percent of Wallet to take position.
        """
        return 0
    
    #To determine short close condition
    def shortCloseConditions(self, lastIndex):
        """
        To determine short close.
        Must return the percent of current short trade to close
        """
        return 100