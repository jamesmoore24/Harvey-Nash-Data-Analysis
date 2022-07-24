"""
Purpose of this script is to use Financial API services to provide full data coverage for the Harvey Nash dataset.
Will need to access all the ticker symbols for the companies listed in the HN dataset that currently intersects with the
dataset that Gio has provided

As a note a future data-entry position could be done to look through all entries in the HN dataset to provide ticker symbols
for the publicly traded companies in the survey. Then we would have a higher sampling quantity and be able to prove significance
more strongly

v 1.0 (7/10/22):
    - Make a spreadsheet with company name, ticker symbol and useful financial information obtained from API
    - Using Selenium with Chromium webdriver to obtain ticker symbols from company names
    - Uses FMP (Financial Modeling Prep) API (250 requests/day) to obtain financial and balance statements for public companeis on HN Survey
    - 

v 1.1 (7/15/22):
    - Switched out FMP API for WRDS (Wharton) for financial data using Compustat
    - Cleaned ticker symbols so that there are no repeats
    - Obtained ratio data for kpi (key performance indicators)
        - Contained within Public_Company_Ratio_Data.xlsx
    - Cleaned ratio data (excluded missing data points/tickers with no data)

v 1.2 (7/21/22):
    - Accessed WRDS for ratios (beta) and used NAICS from fundamental query
    - Cleaned data (dropna)
"""

import datetime
from ipaddress import collapse_addresses
from tkinter.tix import Tree
from click import edit
import pandas as pd
import json
from urllib.request import urlopen
import time
import random
import csv
import re
import yfinance as yf
from bs4 import BeautifulSoup
import requests
from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




###WEBSCRAPER###
#Takes 2-10 seconds/query * ~2000 companies = ~3.33 hours to complete
#Using selenium module with chromium webdriver
#Takes ticker off of google stock page
#Searches "{company} stock" on google and searches for ticker element via XPATH


""" company_list = []
ticker_list = []
exchange_list = []

driver = webdriver.Chrome()

def company_url_converter(company):
    str = ''
    for word in company.split(' '):
        str += word
        str += '+'
    return str

for index, row in survey_df.iterrows():
    company = row['Q45_2']
    if isinstance(company, str):
        company_url = company_url_converter(company)
        driver.get(f'https://www.google.com/search?q={company_url}stock&rlz=1C5CHFA_enUS965US967&oq=apple+stock&aqs=chrome.0.69i59j0i433i512j0i395i433i512l2j0i395i512l2j0i395i433i512l2j0i395i512j0i395i433i512.173798j1j7&sourceid=chrome&ie=UTF-8')
        try:
            #identifying the ticker through XPATH of page
            info = driver.find_element(By.XPATH, '//*[@id="rcnt"]/div[1]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[1]').text.split(' ')

            print(info[1], info[0].split(':')[0])
            ticker_list.append(info[1])
            exchange_list.append(info[0].split(':')[0])
            company_list.append(company)
        except:
            print(f"Can't find ticker for {company}")
        
        #need to sleep so google doesn't know it is a bot
        sleep = random.random()*8+2
        print("Sleeping for " + str(sleep))
        time.sleep(sleep)

d = {'Company Name': company_list, 'Exchange': exchange_list, 'Ticker': ticker_list}
df = pd.DataFrame(data=d)
df.to_excel("tickers.xlsx")  """

###GICS Sector Code Getter

df = pd.read_excel('data_fmp.xlsx')

gics_sector = []
gics_dict = dict()

driver = webdriver.Chrome()

for index, row in df.iterrows():
    if row['symbol'] not in gics_dict:
        ticker = row['symbol']
        
        #query the fidelity website to obtain gics code
        driver.get(f'https://eresearch.fidelity.com/eresearch/evaluate/snapshot.jhtml?symbols={ticker}')
        try:
            info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr/td[4]/table[2]/tbody/tr/td[1]/div[3]/div[8]/span/a"))).text
        except:
            info = ' '
        
        #create new entry for gics sector
        gics_dict[row['symbol']] = info
        gics_sector.append(info)
        sleep = random.random()*3+2
        print("Sleeping for " + str(sleep))
        time.sleep(sleep)
    else:
        gics_sector.append(gics_dict[row['symbol']])
    
    print(gics_sector)
    #need to sleep so google doesn't know it is a bot
    

df['GICS Sector'] = gics_sector

df.to_excel('gics_data_fmp.xlsx')



###FMP API###

""" def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def change_url(ticker, type):
    urls = {
        'fs': 'https://financialmodelingprep.com/api/v3/income-statement/*?limit=120&apikey=f1551f3b93419849190c823376dae33c',
        'bs':'https://financialmodelingprep.com/api/v3/balance-sheet-statement/*?apikey=f1551f3b93419849190c823376dae33c&limit=120',
        'cf': 'https://financialmodelingprep.com/api/v3/cash-flow-statement/*?apikey=f1551f3b93419849190c823376dae33c&limit=120'
    }

    return urls[type].split('*')[0] + ticker + urls[type].split('*')[1]

company_list = []
ticker_list = []
year = []
fs_data = {}

for index, row in ticker_df.iterrows():
    try:
        for year_data in get_jsonparsed_data(change_url(row['Ticker'], 'fs')):
            print(year_data)
            company_list.append(row['Company Name'])
            ticker_list.append(row['Ticker'])
            if len(fs_data) == 0:
                for key in year_data:
                    fs_data[key] = [year_data[key]]
            else:
                for key in year_data:
                    fs_data[key].append(year_data[key])
        print("Got data for " + str(row['Company Name']))
    except:
        print("Couldn't get data for " + str(row['Company Name']))

#concatentate all row data
fs_data = pd.DataFrame(fs_data)

df = pd.DataFrame({
    'Company Name': company_list,
    'Ticker': ticker_list,
})

df = pd.concat([df, fs_data], axis=1, join='inner')

df.to_excel("rest_fs_data.xlsx") """



    
            
            
            


        
        
        
        

