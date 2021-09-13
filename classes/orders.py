class Orders:
    
    @staticmethod
    def setOrderBuy(wallet, percent, price, time):
        to_buy = (wallet.base * percent / 100) / price
        fees =  0.007 * to_buy
        wallet.trade += to_buy - fees
        wallet.base -= wallet.base * percent / 100
        print("Buy BTC at",price,'$ the', time)
        return True
    
    @staticmethod
    def setOrderSell(wallet, percent, price, time):
        to_sell = (wallet.trade * percent / 100) * price
        fees =  0.007 * to_sell
        wallet.base += to_sell - fees
        wallet.trade -= wallet.trade * percent / 100
        print("Sell BTC at",price,'$ the', time)
        return True