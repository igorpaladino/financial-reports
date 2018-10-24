import csv
import datetime
from Report import Report
from Report2 import Report2
from Header import Header
from decimal import Decimal
from tabulate import tabulate
from dateutil.relativedelta import relativedelta

#environment variables
csvPath = "/Users/igorpgcosta/Dropbox/YNAB/Exports/My Budget as of 2018-08-03 1141 PM-Register.csv"

#variables
investments = ["XP Investimentos", "Tesouro Selic XP", "BTG Yield DIFI CP", "DLM Premium 30 FIRF CP LP", "CDB Banco BMG", "AZ Quest Total Return FIM", "Tesouro IPCA+ 2024"]
closedInvestments = ["LCI", "Tesouro Direto", "VGBL", "Poupanca 01", "Poupanca 51"]
dates = ["07/2018", "06/2018", "05/2018", "04/2018", "03/2018", "02/2018", "01/2018"]
inputDates = ["01/2018", "07/2018"] #date begin and date end
profitPayee = "Profits"

allInvestments = investments + closedInvestments

#Budget: iConta, NuConta, Nu Credit Card, Cash, Home, BB Current Account
#Closed Budget: BB Credit Card

reports = []
reports2 = []
balances = []

def diffMonth(startDatetime, endDatetime):
  if startDatetime > endDatetime:
    startDatetime, endDatetime = endDatetime, startDatetime
  return (12 - startDatetime.month + 1) + (endDatetime.year - startDatetime.year - 1) * 12 + endDatetime.month

def nextMonth(datetimeInput):
  return datetimeInput + relativedelta(months=1)

def previousMonth(datetimeInput):
  return datetimeInput - relativedelta(months=1)

def setMonthBalance(reports, records, investments, dates):
  for date in dates:
    date2 = datetime.datetime.strptime(date, '%m/%Y')
    print date2
    balancePerDate = Decimal(0)
    finalBalanceDate = ""
    recordsPerDate = list(filter(lambda record : record[Header.Date].endswith(date) , records))
    for investment in investments:
      specificRecordsPerDate = list(filter(lambda record : record[Header.Account] == investment, recordsPerDate))
      if specificRecordsPerDate:
        balancePerDate += Decimal(specificRecordsPerDate[-1][Header.RunningBalance][2:].replace(',','.'))
      if specificRecordsPerDate and specificRecordsPerDate[-1][Header.Date] > finalBalanceDate:
        finalBalanceDate = specificRecordsPerDate[-1][Header.Date]
    report = list(filter(lambda report : report.date == date, reports))
    if report: report = report[0]
    else: report = Report(date)      
    report.setBalance(balancePerDate, finalBalanceDate)
    reports.append(report)
  return reports

def setMonthProfits(reports, profits, dates):
  for date in dates:
    dateProfitRecords = list(filter(lambda record : record[Header.Date].endswith(date) , profits))
    profitSum = 0
    for record in dateProfitRecords:
      inflow = Decimal(record[Header.Inflow][2:].replace(',','.'))
      outflow = Decimal(record[Header.Outflow][2:].replace(',','.'))
      profitSum = profitSum + inflow - outflow
    report = list(filter(lambda report : report.date ==  date, reports))
    if report: 
      report = report[0] 
    if not report:
      report = Report(date)
      reports.append(report)
    report.profitSum = profitSum
  return reports

def setMonthBalancePerInvestment(reports, records, investments, dates):
  for investment in investments:
    specificRecords = list(filter(lambda record : record[Header.Account] == investment, records))
    for date in dates:
      balancePerDate = Decimal(0)
      finalBalanceDate = ""
      recordsPerDate = list(filter(lambda record : record[Header.Date].endswith(date) , specificRecords))
      if recordsPerDate:
        balancePerDate = Decimal(recordsPerDate[-1][Header.RunningBalance][2:].replace(',','.'))
      if recordsPerDate and recordsPerDate[-1][Header.Date] > finalBalanceDate:
        finalBalanceDate = recordsPerDate[-1][Header.Date]
      report = list(filter(lambda report : report.date == date and report.type == investment, reports))
      if report:
        report = report[0]
      else:
        report = Report2(date)
        reports.append(report)
      report.setFinalBalance(balancePerDate, finalBalanceDate)
      report.type = investment
  return reports

def setMonthProfitsPerInvestment(reports, profits, investments, dates):
  for investment in investments:
    specificProfits = list(filter(lambda record : record[Header.Account] == investment, profits))
    for date in dates:
      profitSum = 0
      profitsPerDate = list(filter(lambda record : record[Header.Date].endswith(date) , specificProfits))
      for record in profitsPerDate:
        inflow = Decimal(record[Header.Inflow][2:].replace(',','.'))
        outflow = Decimal(record[Header.Outflow][2:].replace(',','.'))
        profitSum = profitSum + inflow - outflow        
      report = list(filter(lambda report : report.date == date and report.type == investment, reports))
      if report:
        report = report[0]
      else:
        report = Report2(date)
        reports.append(report)
      if report.finalBalance:
        report.profit = profitSum
        report.minRate = float(profitSum)/float(report.finalBalance)*100.0
  return reports

def setPartialMean(reports):
  for report in reports:
    thisDate = report.date
    filteredReports = list(filter(lambda report: report.date <= thisDate, reports))
    profits = list(map(lambda report: report.profitSum, filteredReports))
    report.profitMean = sum(profits)/len(profits)
  return reports
  
def setInicialBalance(reports):
  for report in reports:
    thisDate = report.date
    previousDate = str(int(report.date[0:2]) - 1).zfill(2)  + report.date[2:]
    previousReport = list(filter(lambda reportIter: reportIter.date == previousDate and report.type == reportIter.type, reports))
    if previousReport:
      previousReport = previousReport[0]
      report.setInitialBalance(previousReport.finalBalance, previousReport.finalBalanceDate)
      if report.initialBalance:
        report.maxRate = float(report.profit)/float(report.initialBalance)*100.0

with open(csvPath, 'rb') as csvfile: #rb => read binary

  spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
  records = list(spamreader)
  investmentRecords = list(filter(lambda record : record[Header.Account] in allInvestments, records))
  profits = list(filter(lambda record : record[Header.Payee] == profitPayee, investmentRecords))

  #get end balance of the month
  reports = setMonthBalance(reports, records, investments, dates)
  #get porfits per month
  reports = setMonthProfits(reports, profits, dates)
  #calculate partial mean
  reports = setPartialMean(reports)
  #get balance investment per month
  reports2 = setMonthBalancePerInvestment(reports2, records, investments, dates)
  #get porfits per month
  reports2 = setMonthProfitsPerInvestment(reports2, profits, investments, dates)
  #set initial balance
  setInicialBalance(reports2)

#report
reportList = list(map(lambda report: report.toList(), reports))
print "\n", tabulate(reportList, Report.headers(), floatfmt=".2f"), "\n"

#mean
profits = list(map(lambda report: report.profitSum, reports))
mean = sum(profits)/len(reports)
print "Mean: {:.2f}\n".format(mean)

#report2
#reportList2 = list(map(lambda report: report.toList(), reports2))
#print "\n", tabulate(reportList2, Report2.headers(), floatfmt=".5f"), "\n"

for investment in investments:
  #print investment
  filteredReports = list(filter(lambda report : report.type == investment, reports2))
  filteredList = list(map(lambda report: report.toList(), filteredReports))
  print tabulate(filteredList, Report2.headers(), floatfmt=".2f"), "\n"
  minRates = list(map(lambda report: report.minRate, filteredReports))
  maxRates = list(map(lambda report: report.maxRate, filteredReports))
  accumulatedMinRate = (reduce( (lambda x, y: x * (1 + y/100.0)) , [1] + minRates[:-1] ) - 1)*100.0
  accumulatedMaxRate = (reduce( (lambda x, y: x * (1 + y/100.0)) , [1] + maxRates[:-1] ) - 1)*100.0  
  print "Acummulated Min Rate: {:.2f}, Acummulated Max Rate: {:.2f} (not considering first month).\n".format(accumulatedMinRate, accumulatedMaxRate)

  #next thing to do: store data in a better way