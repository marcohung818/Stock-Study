import pandas as pd
import numpy as np
import StockDataBase as db #import the Stock List
import yfinance as yf
import time

def getRevenueAndGrossProfit(symbol):
    stockTicker = yf.Ticker(symbol)
    getAnnuallyGrossProfit(stockTicker)
    getQuarterlyGrossProfit(stockTicker)
    getAnnuallyRevenue(stockTicker)
    getQuarterlyRevenue(stockTicker)

def getAnnuallyGrossProfit(ticker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)

def getQuarterlyGrossProfit(ticker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.quarterly_financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)

def getAnnuallyRevenue(ticker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)

def getQuarterlyRevenue(ticker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.quarterly_financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)

def getStockDataMain(symbol):
    getRevenueAndGrossProfit(symbol)
    return

#Pass the data - return 1. Percentage Changed(Size = 3) 2. Score(Size = 3) 3.totalScore(Size = 1)
def countingMachine(data):
    period_to_get = 4
    print(data)
    #return empty array if no data
    if not data or (len(data) < period_to_get):
        return [None]*period_to_get, [None]*period_to_get, None
    else:
        score = []
        changedPercentage = []
        #Calculate the change
        for i in range(0, period_to_get - 1):
            Changed = ((data[i] + data[i + 1]) / data[i + 1] - 0.0000001) * 100
            changedPercentage.append(round(Changed, 2))
        #Calculate the Score
        score = [2**((period_to_get-1)-1-index) if change >= 0 else 0 for index, change in enumerate(changedPercentage)]
        # sum of score
        totalScore = sum(score)
        return changedPercentage, score, totalScore

def main():
    print("Please input the Stock Symbol")
    symbol = input()
    #getStockDataMain(symbol)
    test = [20, -20, 20]
    testpd = pd.DataFrame()
    testpd.append(test)
    print(testpd)
    return

main()
