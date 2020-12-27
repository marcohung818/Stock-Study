import pandas as pd
import numpy as np
import StockDataBase as db #import the Stock List
import yfinance as yf
import time

def getStockDataMain(symbol):
    AAPLstock = yf.Ticker('APD')
    print(AAPLstock.financials)
    print(AAPLstock.balance_sheet)
    print(AAPLstock.cashflow)
    print(AAPLstock.earnings)
    print(AAPLstock.info)
    print(AAPLstock.splits)

def main():
    print("Please input the Stock Symbol")
    symbol = input()
    getStockDataMain(symbol)

main()
