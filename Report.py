from decimal import Decimal
from Header import Header

class Report:
    def __init__(self, date, profitSum = Decimal(0), finalBalance = Decimal(0), finalBalanceDate = '', profitMean = Decimal(0)):
        self.date = date
        self.profitSum = profitSum
        self.finalBalance = finalBalance
        self.finalBalanceDate = finalBalanceDate
        self.profitMean = profitMean

    def setBalance(self, finalBalance, finalBalanceDate):
        self.finalBalance = finalBalance
        self.finalBalanceDate = finalBalanceDate

    def printClass(self):
      print self.date, self.profitSum

    def toList(self):
      return [self.date, self.profitSum, self.finalBalance, self.finalBalanceDate, self.profitMean]

    @staticmethod
    def headers():
      return ["Month Date", "Profits", "Final Balance", "Final Balance Date", "Profit Mean"]

    

    
    