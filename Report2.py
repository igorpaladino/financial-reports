from decimal import Decimal
from Header import Header

class Report2:
    def __init__(self, date, type = "", finalBalance = Decimal(0), finalBalanceDate = '', initialBalance = Decimal(0), initialBalanceDate = '', profit = Decimal(0), minRate = 0, maxRate = 0):
        self.date = date
        self.type = type #BTG, VGBL, ...
        self.finalBalance = finalBalance
        self.finalBalanceDate = finalBalanceDate
        self.initialBalance = initialBalance
        self.initialBalanceDate = initialBalanceDate
        self.profit = profit
        self.minRate = minRate
        self.maxRate = maxRate

    def setFinalBalance(self, finalBalance, finalBalanceDate):
        self.finalBalance = finalBalance
        self.finalBalanceDate = finalBalanceDate

    def setInitialBalance(self, initialBalance, initialBalanceDate):
        self.initialBalance = initialBalance
        self.initialBalanceDate = initialBalanceDate

    def printClass(self):
      print self.date, self.type, self.finalBalance, self.finalBalanceDate, self.minRate, self.maxRate

    def toList(self):
      return [self.date, self.type, self.profit, self.initialBalance, self.initialBalanceDate, self.finalBalance, self.finalBalanceDate, self.minRate, self.maxRate]

    @staticmethod
    def headers():
      return ["Month Date", "Type", "Profit", "Initial Balance",  "Initial Balance Date", "Final Balance",  "Final Balance Date", "Min Rate(%)", "Max Rate(%)"]

    

    
    