from decimal import *

class Lot:

    standard = Decimal(100000)
    mini = Decimal(10000)
    micro = Decimal(1000)

    size = None
    amount = None
    leverage = None

    def __init__(self, amount, maxLeverage):
        if Lot.standard / amount <= maxLeverage:
            self.size = Lot.standard
        if self.size == None and Lot.mini / amount <= maxLeverage:
            self.size = Lot.mini
        if self.size == None and Lot.micro / amount <= maxLeverage:
            self.size = Lot.mini
        self.amount = amount
        self.leverage = self.size / self.amount
