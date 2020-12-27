import pandas as pd
import numpy as np
import time
import Reuters_StockDataBase as db #import the Stock List
import requests

dataFrameCols = ["Stock", "Fiscal Period", "Quarterly EPS Score", "Quarterly EPS Changed %", "Annual EPS Score", "Annual EPS Changed %", "Quarterly Revenue Score", "Quarterly Revenue Changed %", "Annual Revenue Score", "Annual Revenue Changed %", "Quarterly Gross Profit Score", "Quarterly Gross Profit Changed %", "Annual Gross Profit Score", "Annual Gross Profit Changed %"]

URL_BASE = 'https://www.reuters.com'
URL_API_BASE = 'https://www.reuters.com/companies/api/getFetchCompanyFinancials/{}'

# period to get
period_to_get = 4

# calculate percentage changed
def getPercentageChange(l, period_to_get=period_to_get):
    try:
        # get required periods only
        # assume latest data come first
        l = l[:period_to_get]
        l = [float(x) for x in l]
    except:
        return []
    # added np.sign to deal with positive -> negative/ negative -> positive cases
    changed = [round(np.sign(l[i+1]) * 100 * (l[i] - l[i+1])/(l[i+1]+(np.sign(l[i+1])*0.000001)), 2) for i in range(0, period_to_get-1)]
    return changed

#Calculate the Score
def getScore(l, period_to_get=period_to_get):
    try:
        # get required periods only
        # assume latest data come first
        l = l[:period_to_get]
        l = [float(x) for x in l]
    except:
        return []
    score = [2**((period_to_get-1)-1-i) if l[i] >= 0 else 0 for i in range(0, period_to_get-1)]
    return score

# --------------------- Scraping --------------------#
def fetch(symbols):
    
    raw_data = []
    
    for symbol in symbols:
    
        URL_API = URL_API_BASE.format(symbol.upper())
        while (True):
            r = requests.get(URL_API)
            time.sleep(5)
            if 'market_data' in r.json().keys():
                raw_data.append(r.json())
                break
            else:
                print(f'Rescraping {symbol}')
                time.sleep(5)
            
    print('End of fetching')
    return raw_data

# for parsing
# index order
index_order = ['Quarterly Diluted Normalized EPS', 'Quarterly Revenue', 'Quarterly Gross Profit', 'Annual Diluted Normalized EPS', 'Annual Revenue', 'Annual Gross Profit']
def parse(raw_data):
    
    parsed_data = []
    parsed_data_score = []
    
    ### loop each stock
    for data in raw_data:
    
        ## list of data
        try:
            data_list = [
                    data['market_data']['financial_statements']['income']['interim']['Diluted Normalized EPS'],
                    data['market_data']['financial_statements']['income']['interim']['Total Revenue'],
                    data['market_data']['financial_statements']['income']['interim']['Gross Profit'],
                    data['market_data']['financial_statements']['income']['annual']['Diluted Normalized EPS'],
                    data['market_data']['financial_statements']['income']['annual']['Total Revenue'],
                    data['market_data']['financial_statements']['income']['annual']['Gross Profit']
                    ]
        except:
            1/0
            for i in range(10):
                print("******************")
            print(f"Skipped {data['ric']}")
            for i in range(10):
                print("******************")
            time.sleep(1)
            continue
            
        #------------------------------- Calculate Scores---------------------------#
        # list of values
        value_list = [[float(x['value']) for x in d] for d in data_list]

        # list of percentage change
        percentageChange_list = [getPercentageChange(v) for v in value_list]

        # list of scores
        score_list = [getScore(v) for v in percentageChange_list]
        scoreTotal_list = [sum(score) for score in score_list]
        
        # list of sign of new value
        sign_list = [['P' if np.sign(v) == 1 else 'N' for v in vs[:period_to_get-1]] for vs in value_list]
        
        ### period data
        for period in range(0, period_to_get-1):
            output = {
                    'Stock': data['ric'],
                    'Fiscal Period': period + 1,
                    }
            for i, name in enumerate(index_order):
                output[f'{name} Score'] = score_list[i][period]
                output[f'{name} % Change'] = percentageChange_list[i][period]
                output[f'{name} Sign'] = sign_list[i][period]
            parsed_data.append(output)
        
        ### final score
        output_score = {
            'Stock': data['ric'],
            }
        
        for i, name in enumerate(index_order):
            output_score[f'{name} Total Score'] = scoreTotal_list[i]
        parsed_data_score.append(output_score)
        
    print('End of parsing')
    return parsed_data, parsed_data_score

def store(parsed_data, parsed_data_score, industry):
    
    df = pd.DataFrame(parsed_data, columns=parsed_data[0].keys())
    df_score = pd.DataFrame(parsed_data_score, columns=parsed_data_score[0].keys())

    df.to_csv(f"SP500_{industry}.csv", index=False)
    df_score.to_csv(f"SP500_{industry}_score.csv", index=False)
    
    print('End of storing')
    
for industry, stocks in db.SP500.items():
    
    if industry in ['Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive', 'Energy']:
        continue
    
    print(f'Start scraping {industry}')
    raw_data = fetch(stocks)
    parsed_data, parsed_data_score = parse(raw_data)
    store(parsed_data, parsed_data_score, industry)
    print(f'End of scraping {industry}')
        
#main()
