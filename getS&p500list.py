import requests
import pandas as pd
import yfinance as yf
import time
# 貼上連結

currentStocks = []
IndustriesClassification = ['Technology', 'Consumer Cyclical', 'Communication Services', 'Financial Services', 'Healthcare', 'Consumer Defensive', 'Energy', 'Industrials', 'Utilities', 'Basic Materials', 'Real Estate']
url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
sp500_request = requests.get(url, headers = headers)
sp500_data = pd.read_html(sp500_request.text)[0]
# 欄位『Symbol』就是股票代碼
sp500_stock_name = sp500_data.Symbol
# 用 replace 將符號進行替換
sp500_list = sp500_stock_name.apply(lambda x: x.replace('.', '-'))

#由股票種類得出對應的股票
def get_sp500_info_by_sector():
    print("Please Input The Require Sector, You can select from below")
    for i in range(len(IndustriesClassification)):
        print(str(i + 1) + ". " + IndustriesClassification[i])
    return

#分別股票種類
def get_sp500_sector_Classification():
    for i in sp500_list:
        try:
            if((yf.Ticker(i).info)['sector']) not in IndustriesClassification:
                IndustriesClassification.append((yf.Ticker(i).info)['sector'])
        except KeyError:
            continue

def get_single_stock_info():
    print("Please input the Stock Symbol")
    stockInput = input()
    try:
        print((yf.Ticker(stockInput).info)['sector'])
    except KeyError:
        print("error")
def main():
    while(1):
        print(" ")
        print("1. Get SP500 Industries Classification")
        print("2. Get SP500 Data By Industries")
        print("3. Get Single Data")
        print("Exit. Quit the program")
        print("Please input your Request")
        fInput = input()
        if(fInput == "1"):
            get_sp500_sector_Classification()
        elif(fInput == "2"):
            get_sp500_info_by_sector()
        elif(fInput == "3"):
            get_single_stock_info()
        elif(fInput == "exit"):
            return



main()
