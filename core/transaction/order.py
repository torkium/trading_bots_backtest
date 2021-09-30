from decimal import *

class Order:
    ORDER_TYPE_BUY = "buy"
    ORDER_TYPE_SELL = "sell"
    __TYPE_ALLOWED = ["buy", "sell"]
    __type = None
    __amount = None
    __finalAmount = None
    __fees = None
    __price = None
    __baseCurrency = None
    __tradeCurrency = None
    __time = None

    def __init__(self, type, amount, fees, price, baseCurrency, tradeCurrency, time, checkAllowed=True) -> None:
        if checkAllowed and type not in self.__TYPE_ALLOWED:
            raise Exception("Class Order accept only these values for argument 'type' : " + ", ".join(self.__TYPE_ALLOWED))
        self.__type = type
        self.__amount = Decimal(amount)
        self.__fees = Decimal(fees)
        self.__price = Decimal(price)
        self.__time = time
        self.__baseCurrency = baseCurrency
        self.__tradeCurrency = tradeCurrency

    @property
    def type(self):
        return self.__type

    @property
    def amount(self):
        return self.__amount

    @property
    def finalAmount(self):
        return self.__finalAmount

    @property
    def percentGain(self):
        if self.__finalAmount != None:
            return (self.__finalAmount-self.__amount)*100/self.__amount
        return None

    @property
    def fees(self):
        return self.__fees

    @property
    def price(self):
        return self.__price

    @property
    def baseCurrency(self):
        return self.__baseCurrency

    @property
    def tradeCurrency(self):
        return self.__tradeCurrency

    @property
    def time(self):
        return self.__time

    @finalAmount.setter
    def finalAmount(self, value):
        self.__finalAmount = value

    def __str__(self):
        str = f"\n--------------Order Status--------------\n"
        str += f"Date : {self.__time}\n"
        str += f"Type : {self.__type}\n"
        str += f"Amount : {self.__amount} {self.__baseCurrency}\n"
        str += f"Fees : {self.__fees} {self.__tradeCurrency}\n"
        str += f"Price : {self.__price} {self.__tradeCurrency}\n"
        str += f"--------------Order Status--------------\n"
        return str