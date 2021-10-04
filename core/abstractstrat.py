from core.wallet import Wallet
from decimal import *

class AbstractStrat:
    exchange = False
    historic = False
    wallet = False
    step = "main"
    baseCurrency = None
    tradingCurrency = None
    mainTimeFrame = None
    startDate = None
    endDate = None
    base = None
    trade = None
    transactions = None
    history = None
    startWallet = None
    minWallet = None
    maxWallet = None
    currentDrawdown = None
    maxDrawdown = None
    totalFees = None

    def __init__(self, exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame):
        self.exchange = exchange
        self.mainTimeFrame = mainTimeFrame
        self.wallet = Wallet(baseCurrency, tradingCurrency, base, trade)
        self.baseCurrency = baseCurrency
        self.tradingCurrency = tradingCurrency
        self.base = base
        self.trade = trade
        self.transactions = {}
        self.history = {}
        self.currentDrawdown = 0
        self.maxDrawdown = 0
        self.totalFees = 0

    
    def setIndicators(self, timeframe):
        return None

    def backtest(self):
        """
        To launch backtest on strat
        """
        return None

    def initBacktest(self, startDate, endDate=None):
        """
        To launch backtest on strat
        """
        self.exchange.getHistoric(self.tradingCurrency, self.baseCurrency, self.mainTimeFrame, startDate, endDate)
        self.startDate = startDate
        self.endDate = endDate
        self.startWallet = self.wallet.getTotalAmount(self.exchange.historic[self.mainTimeFrame]['open'].iloc[0])
        self.minWallet = self.startWallet
        self.maxWallet = self.startWallet
        return None

    def demo(self):
        """
        To launch strat in live demo mode
        """
        return None

    def run(self, client, apiKey, apiSecret):
        self.client = client(apiKey, apiSecret)
        #TODO : Take in account timeframe and max indicators period to determinate start date history
        self.exchange.historic[self.mainTimeFrame] = self.exchange.getHistoric(self.tradingCurrency, self.baseCurrency, self.mainTimeFrame, "1 day ago UTC").tail(500)
        self.startWallet = self.wallet.getTotalAmount(self.exchange.historic[self.mainTimeFrame]['open'].iloc[0])
        self.minWallet = self.startWallet
        self.maxWallet = self.startWallet
        self.exchange.waitNewCandle(self.newCandleCallback, self.tradingCurrency+self.baseCurrency, self.mainTimeFrame, apiKey, apiSecret)

    def newCandleCallback(self, msg):
        self.exchange.appendNewCandle(msg, self.mainTimeFrame, self.tradingCurrency+self.baseCurrency)
        self.setIndicators(self.mainTimeFrame)
        return None

    def getFinalLog(self):
        finalLog = "Wallet From " + str(self.startWallet) + " " + self.wallet.baseCurrency + " to " + str(self.wallet.getTotalAmount(self.exchange.historic[self.mainTimeFrame]['close'].iloc[-1])) + " " + self.wallet.baseCurrency + " (" + str((self.wallet.getTotalAmount(self.exchange.historic[self.mainTimeFrame]['close'].iloc[-1])-self.startWallet)*100/self.startWallet) + "%)\n"
        finalLog += "Total fees : " + str(self.totalFees) + " " + self.wallet.baseCurrency + "\n"
        finalLog += "Buy & hold From " + str(self.startWallet) + " " + self.wallet.baseCurrency + " to " + str(self.startWallet * self.exchange.historic[self.mainTimeFrame]['close'].iloc[-1] / self.exchange.historic[self.mainTimeFrame]['open'].iloc[0]) + " " + self.wallet.baseCurrency + " (" + str((self.startWallet * self.exchange.historic[self.mainTimeFrame]['close'].iloc[-1] / self.exchange.historic[self.mainTimeFrame]['open'].iloc[0]-self.startWallet)*100/self.startWallet) + "%)\n"
        transactions_type = {}
        for key in self.transactions:
            if not self.transactions[key].type in transactions_type:
                transactions_type[self.transactions[key].type] = 0
            transactions_type[self.transactions[key].type] += 1
        for key in transactions_type:
            finalLog += key + " : " + str(transactions_type[key]) + "\n"
        finalLog += "Min Wallet : " + str(self.minWallet) + " " + self.wallet.baseCurrency + "\n"
        finalLog += "Max Wallet : " + str(self.maxWallet) + " " + self.wallet.baseCurrency + "\n"
        finalLog += "Max Drawdown : " + str(self.maxDrawdown) + "%"
        return finalLog

    def addTransaction(self, transaction, wallet, index):
        self.totalFees += transaction.fees
        self.history[index] = {"from":{"base":wallet.base,"trade":wallet.trade},"to":{"base":wallet.base,"trade":wallet.trade}, "drawdown": 0}
        if transaction.action == "buy":
            wallet.trade += Decimal(transaction.amount)
            wallet.base -= transaction.amount*transaction.price + transaction.fees
        if transaction.action == "sell":
            wallet.trade -= Decimal(transaction.amount)
            wallet.base += transaction.amount*transaction.price - transaction.fees
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

    def addHistory(self, timeframe):
        self.exchange.historic[timeframe] = self.exchange.getHistoric(self.tradingCurrency, self.baseCurrency, timeframe, self.startDate, self.endDate)

    def getLastHistoryIndex(self, index, timeframe):
        timeToReturn = None
        for key in self.exchange.historic[timeframe]:
            if key >= index:
                return timeToReturn
            timeToReturn = key