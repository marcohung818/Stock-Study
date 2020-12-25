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
#nasdaqEarningUrlFormat = "https://www.nasdaq.com/market-activity/stocks/aapl/earnings" For the Quarterly EPS
#nasdaqFinancialUrlFormat = "https://www.nasdaq.com/market-activity/stocks/aapl/financials" For the Quarterly / Annually Financial
dataFrameCols = ["Fiscal Period", "Quarterly EPS Score", "Quarterly EPS Changed %", "Annual EPS Score", "Annual EPS Changed %", "Quarterly Revenue Score", "Quarterly Revenue Changed %", "Annual Revenue Score", "Annual Revenue Changed %", "Quarterly Gross Profit Score", "Quarterly Gross Profit Changed %", "Annual Gross Profit Score", "Annual Gross Profit Changed %"]
#The Most important Data output
output = pd.DataFrame(columns=dataFrameCols)

#Program Functions
#The Main Get Stock Function
def getStockDataMain(symbol):
    quarterlyEpsChanged, quarterlyEpsScore = getStockQuarterlyEPS(symbol)
    quarterlyRevenueChanged, quarterlyRevenueScore = getStockQuarterlyRevenue(symbol)
    quarterlyGrossProfitChanged, quarterlyGrossProfitScore = getStockQuarterlyGrossProfit(symbol)
    annuallyRevenueChanged, annuallyRevenueScore = getStockAnnualRevenue(symbol)
    annuallyGrossProfitChanged, annuallyGrossProfitScore = getStockAnnualGrossProfit(symbol)

    print(quarterlyGrossProfitChanged)
    print(quarterlyGrossProfitScore)
    #getStockQuarterlyEPS(symbol)
    return

#Get and Calculate the Quarterly Data
#Get the Quarterly EPS -  return 1.EpsChanged 2.EpsScore
def getStockQuarterlyEPS(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/earnings")
    EpsData = []
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[3]/div/div/table/tbody[2]/tr[1]/td[2]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[3]/div/div/table/tbody[2]/tr["
        #Get the Value of the EPS
        for i in range(1, 5):
            EpsData.append(float(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]/td[2]").text))
    except:
        driver.quit()
        print("Error in QuarterlyEPS")
    return countingMachine(EpsData)
#Get the Quarterly Revenue - return 1.RevenueChanged 2.RevenueScore
def getStockQuarterlyRevenue(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/financials")
    RevenueData = []
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        mainPageLoaded.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/button").click()
        mainPageLoaded.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div/button[2]").click()
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[1]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td["
        #Get the Value of the Revenue
        for i in range(1, 5):
            RevenueData.append(float(removeSpcialCharacter(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]").text)))
    except:
        driver.quit()
        print("Error in AnnualRevenue")
    return countingMachine(RevenueData)
#Get the Quarterly Gross Profit - return 1.GrossProfitChanged 2.GrossProfitScore
def getStockQuarterlyGrossProfit(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/financials")
    GrossProfitData = []
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        mainPageLoaded.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/button").click()
        mainPageLoaded.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div/button[2]").click()
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[3]/td[1]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[3]/td["
        #Get the Value of the Revenue
        for i in range(1, 5):
            GrossProfitData.append(float(removeSpcialCharacter(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]").text)))
    except:
        driver.quit()
        print("Error in QuarterlyGrossProfit")
    return countingMachine(GrossProfitData)

#Get and Calculate the Annual Data
#Get the Annually Revenue - return 1.RevenueChanged 2.RevenueScore
def getStockAnnualRevenue(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/financials")
    RevenueData = []
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[1]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td["
        #Get the Value of the Revenue
        for i in range(1, 5):
            RevenueData.append(float(removeSpcialCharacter(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]").text)))
    except:
        driver.quit()
        print("Error in AnnualRevenue")
    return countingMachine(RevenueData)
#Get the Annually Gross Profit - return 1.GrossProfitChanged 2.GrossProfitScore
def getStockAnnualGrossProfit(symbol):
    driver.get("https://www.nasdaq.com/market-activity/stocks/" + str(symbol) + "/financials")
    GrossProfitData = []
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[3]/td[1]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/table/tbody/tr[3]/td["
        #Get the Value of the Revenue
        for i in range(1, 5):
            GrossProfitData.append(float(removeSpcialCharacter(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]").text)))
    except:
        driver.quit()
        print("Error in AnnualGrossProfit")
    return countingMachine(GrossProfitData)

#Pass the data - return 1. Percentage Changed 2. Score
def countingMachine(data):
    print(data)
    score = []
    changedPercentage = []
    #Calculate the change
    for i in range(0, 3):
        Changed = ((data[i] - data[i+1]) / data[i+1]) * 100
        changedPercentage.append(round(Changed, 2))
    #Calculate the Score
    if(changedPercentage[0] >= 0):
        score.append(4)
    else:
        score.append(0)
    if(changedPercentage[1] >= 0):
        score.append(2)
    else:
        score.append(0)
    if(changedPercentage[2] >= 0):
        score.append(1)
    else:
        score.append(0)
    return changedPercentage, score
#Cancel the Special Character - return a string can transfer to float
def removeSpcialCharacter(string):
    outputString = ""
    for character in string:
        if character.isalnum():
            outputString += character
    return outputString

#Check Mode Functions
def checkModeMain():
    while(1):
        print("")
        print("checkeps - Check the EPS data location")
        print("exit - Exit the Check Mode")
        checkModeMainInput = input()
        if(checkModeMainInput == "checkeps"):
            checkStockQuarterlyEPS()
        else:
            return
#Check the Quarterly EPS Location
def checkStockQuarterlyEPS():
    driver.get("https://www.nasdaq.com/market-activity/stocks/aapl/earnings")
    try:
        mainPageLoaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        #Xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[3]/div/div/table/tbody[2]/tr[1]/td[2]"
        Xpth = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[3]/div/div/table/tbody[2]/tr["
        #Get the Value of the EPS
        for i in range(1, 5):
            print(float(mainPageLoaded.find_element_by_xpath(Xpth + str(i) +"]/td[2]").text))
    except:
        driver.quit()
        print("error")
    return

def main():
    while(1):
        print("Stock Symbol - Run the program")
        print("check - Check Mode")
        print("exit - Exit the Program")
        mainInput = input()
        if(mainInput == "exit"):
            return
        elif(mainInput == "check"):
            checkModeMain()
        else:
            getStockDataMain(mainInput)

main()
