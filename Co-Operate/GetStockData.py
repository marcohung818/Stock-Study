import pandas as pd
import numpy as np
import StockDataBase as db #import the Stock List
import yfinance as yf
import time

#Global Values
period_to_get = 4
stocksNormalData = []
stocksTotalScore = []

def getRevenueAndGrossProfit(symbol):
    stockTicker = yf.Ticker(symbol)
    print(stockTicker.financials)
    print(stockTicker.quarterly_financials)
    qGpChanged, qGpScore, qGpTotalScore = getQuarterlyGrossProfit(stockTicker)
    aGpChanged, aGpScore, aGpTotalScore = getAnnuallyGrossProfit(stockTicker)
    qRChanged, qRScore, qRTotalScore = getQuarterlyRevenue(stockTicker)
    aRChanged, aRScore, aRTotalScore = getAnnuallyRevenue(stockTicker)
    '''
    input the data into an array
    for i in range(0, period_to_get - 1):
        array = []
        array.append(aGpScore)
        array.append(aGpChanged)
        array.append(qGpScore)
        array.append(qGpChanged)
        array.append(aRChanged)
        array.append(aRScore)
        array.append(qRChanged)
        array.append(qRScore)
        stocksNormalData.append(array)
    for i in range(0, period_to_get - 1)
        array = []
        array.append(qGpTotalScore)
        array.append(aGpTotalScore)
        array.append(qRTotalScore)
        array.append(aRTotalScore)
        stocksTotalScore.append(array)
    '''

def getAnnuallyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)

def getQuarterlyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.quarterly_financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)

def getAnnuallyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)

def getQuarterlyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.quarterly_financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)

def getStockDataMain(symbol):
    getRevenueAndGrossProfit(symbol)
    return

#Pass the data - return 1. Percentage Changed(Size = 3) 2. Score(Size = 3) 3.totalScore(Size = 1)
def countingMachine(data):

    print(data)
    return [None]*period_to_get, [None]*period_to_get, None
    #return empty array if no data
    '''
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
    '''
def main():
    print("Please input the Stock Symbol")
    symbol = input()
    getStockDataMain(symbol)
    return

main()
