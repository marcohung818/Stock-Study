from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import StockDataBase as db #import the Stock List
chromeDriverPATH = "chromedriver.exe"
driver = webdriver.Chrome(chromeDriverPATH)
#nasdaqEarningUrlFormat = "https://www.nasdaq.com/market-activity/stocks/aapl/earnings"


def getStockData(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/earnings")
    #try:
    mainPageLoaded = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body"))
    )
    epstbodyXpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[3]/div/div/table/tbody"
    epstbodies = mainPageLoaded.find_elements_by_xpath(epstbodyXpath)
    for i in range(2, 5):
        print((mainPageLoaded.find_element_by_xpath(epstbodyXpath + "[1]/" +"tr/th[" + str(i) + "]" )).text)
    #print(len(tbody))
    #except:
        #driver.quit()
        #print("error")
    return

def main():
    while(1):
        print("Input the Stock Symbol or quit the program by \"exit\"")
        mainInput = input()
        if(mainInput != "exit"):
            getStockData(mainInput)
        else:
            return

main()
