import pandas as pd
import numpy as np
import StockDataBase as db #import the Stock List
import yfinance as yf
import time

def getRevenueGrossProfit(symbol):
    stockTicker = yf.Ticker(symbol)
    print(stockTicker .financials)

def getStockDataMain(symbol):
    getRevenueGrossProfit(symbol)

def main():
    print("Please input the Stock Symbol")
    symbol = input()
    getStockDataMain(symbol)

main()
