import requests
import pandas as pd
import yfinance as yf
import time
# 貼上連結

currentStocks = []

url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
sp500_request = requests.get(url, headers = headers)
sp500_data = pd.read_html(sp500_request.text)[0]
# 欄位『Symbol』就是股票代碼
sp500_stock_name = sp500_data.Symbol
# 用 replace 將符號進行替換
sp500_list = sp500_stock_name.apply(lambda x: x.replace('.', '-'))

def get_sp500_info_sector():
    #分別股票種類
    for i in sp500_list:
        if((yf.Ticker(i).info)['sector'] == 'Technology'):
            print(i + "*")
        else:
            print(i)
    return

def main():
    while(1):
        print("1. Get SP500 Industries Classification")
        print("Exit. Quit the program")
        print("Please input your Request")
        fInput = input()
        if(fInput == "1"):
            get_sp500_info_sector()
        elif(fInput == "exit"):
            return



main()
