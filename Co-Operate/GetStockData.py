import pandas as pd
import numpy as np
import StockDataBase as SP500_normal_db #import the Stock List
import Reuters_StockDataBase as db #import the Stock List
import requests
import yfinance as yf
import time

#Global Values
period_to_get = 4
URL_BASE = 'https://www.reuters.com'
URL_API_BASE = 'https://www.reuters.com/companies/api/getFetchCompanyFinancials/{}'

#Get the Revenue and GrossProfit by yfinance Library - return 1. qGpChanged 2. qGpScore 3.qGpTotalScore 4.aGpChanged 5. aGpScore 6. aGpTotalScore 7. qRChanged 8. qRScore 9. qRTotalScore 10. aRChanged 11. aRScore 12. aRTotalScore (All Size = 3)
def getRevenueAndGrossProfit(symbol):
    stockTicker = yf.Ticker(symbol)
    qGpChanged, qGpScore, qGpTotalScore = getQuarterlyGrossProfit(stockTicker)
    aGpChanged, aGpScore, aGpTotalScore = getAnnuallyGrossProfit(stockTicker)
    qRChanged, qRScore, qRTotalScore = getQuarterlyRevenue(stockTicker)
    aRChanged, aRScore, aRTotalScore = getAnnuallyRevenue(stockTicker)
    return qGpChanged, qGpScore, qGpTotalScore, aGpChanged, aGpScore, aGpTotalScore, qRChanged, qRScore, qRTotalScore, aRChanged, aRScore, aRTotalScore
# Get the Annually Gross Profit by yfinance financials location - return 1. countingMachine(grossProfit)
def getAnnuallyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)
# Get the Quarterly Gross Profit by yfinance financials location - return 1. countingMachine(grossProfit)
def getQuarterlyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.quarterly_financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)
# Get the Annually Revenue by yfinance financials location - return 1. countingMachine(revenue)
def getAnnuallyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)
# Get the Quarterly Revenue by yfinance financials location - return 1. countingMachine(revenue)
def getQuarterlyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.quarterly_financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)
# Get the Eps Data
def getEps(symbol):
    return
# Get the Quarterly Eps by request
def getQuarterlyEps(symbol):
    return
# Get the Annually Eps by request
def getAnnuallyEps(symbol):
    return
#The Main function to get and cal the stock data - return 1. normalArrays(Size = 14) 2. totalArrays(Size = 8)
def getStockDataMain(symbol):
    normalArrays = []
    totalArrays = []
    qGpChanged, qGpScore, qGpTotalScore, aGpChanged, aGpScore, aGpTotalScore, qRChanged, qRScore, qRTotalScore, aRChanged, aRScore, aRTotalScore = getRevenueAndGrossProfit(symbol)
    #input the data into an array
    for i in range(0, period_to_get - 1):
        array = [symbol, i + 1, qGpScore[i], qGpChanged[i], aGpScore[i], aGpChanged[i], qRScore[i], qRChanged[i], aRScore[i], aRChanged[i], None, None, None, None]
        normalArrays.append(array)
    totalArray = [symbol, qGpTotalScore, aGpTotalScore, qRTotalScore, aRTotalScore, None, None]
    totalArray.append(calSum((totalArray)))
    totalArrays.append(totalArray)
    return normalArrays, totalArrays


#Pass the data - return 1. Percentage Changed(Size = 3) 2. Score(Size = 3) 3.totalScore(Size = 1)
def countingMachine(data):
    print(data)
    #return empty array if no data
    if not data or (len(data) < period_to_get):
        return [None]*period_to_get, [None]*period_to_get, None
    else:
        score = []
        changedPercentage = []
        #Calculate the change
        for i in range(0, period_to_get - 1):
            Changed = ((data[i] - data[i + 1]) / data[i + 1] - 0.0000001) * 100
            if (data[i + 1] < 0 and data[i] > 0) or (data[i + 1] < 0 and data[i] < 0 and data[i] < data[i + 1]):
                Changed *= -1
            changedPercentage.append(round(Changed, 2))
        #Calculate the Score
        score = [2**((period_to_get-1)-1-index) if change >= 0 else 0 for index, change in enumerate(changedPercentage)]
        # sum of score
        totalScore = sum(score)
        return changedPercentage, score, totalScore

#Calculate the sum of the multiple ddata type array - return 1. Sum of the Array(Size = 1)
def calSum(array):
    sum = 0
    for i in array:
        if i is not None and type(i) == int:
            sum += i
    return sum

def main():
    normalDataFrameCols = ["Stock", "Period", "Quarterly Gross Profit Score", "Quarterly Gross Profit Changed %", "Annual Gross Profit Score", "Annual Gross Profit Changed %", "Quarterly Revenue Score", "Quarterly Revenue Changed %", "Annual Revenue Score", "Annual Revenue Changed %", "Quarterly EPS Score", "Quarterly EPS Changed %", "Annual EPS Score", "Annual EPS Changed %"]
    totalDataFrameCols = ["Stock", "Total Quarterly Gross Profit Score", "Total Annual Gross Profit Score", "Total Quarterly Revenue Score", "Total Annual Revenue Score", "Total Quarterly EPS Score", "Total Annual EPS Score", "Total Score"]
    for industry, stocks in SP500_normal_db.SP500.items():
        normalArrays = []
        totalArrays = []
        for stock in stocks:
            try:
                mainArray = getStockDataMain(stock)
                normalArrays +=  mainArray[0]
                totalArrays += mainArray[1]
            except:
                print("Skipped " + str(stock))
        normalDataOutput = pd.DataFrame(normalArrays, columns = normalDataFrameCols)
        totalScoreOutput = pd.DataFrame(totalArrays, columns = totalDataFrameCols)
        normalDataOutput.to_csv("SP500_NormalData_" + str(industry) + ".csv", index = False)
        totalScoreOutput.to_csv("SP500_TotalScore_" + str(industry) + ".csv" , index = False)
        print("End of scraping" + str(industry))
    return

main()
