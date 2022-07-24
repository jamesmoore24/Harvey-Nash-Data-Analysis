import os
import sys
import typing
import json
import fmpsdk
from dotenv import load_dotenv
import pandas as pd

def getRatio(tickerList, dataPoints):
    """
    Parameters

    Outputs a spreadsheet 
    """
    load_dotenv()
    apikey = os.environ.get("APIKEY")

    #initialize dataset to be made 
    df = pd.DataFrame(columns=dataPoints)

    def yearData(dict):
        """
        Parameters:
            - dict: Dictionary with possible data points

        Returns:
            - listVal: List of values associated with the keys specifed above
        """
        listVals = []

        for key in dataPoints:
            try:
                listVals.append(dict[key])
            except:
                #if there isn't a datapoint for the certain ticker
                listVals.append('None')
        
        return listVals


    for ticker in tickerList:
        try:
            for dict in fmpsdk.financial_ratios(apikey=apikey, symbol=ticker):
                #add row to dataframe
                df.loc[len(df.index)] = yearData(dict)
        except:
            continue

    df.to_excel('data_fmp_rest.xlsx')

tickers = []

for line in open('list_tickers.txt', 'r').readlines():
    tickers.append(line.split('\n')[0])

getRatio(tickers, ['symbol', 'date', 'currentRatio', 'quickRatio', 'cashRatio', 'netProfitMargin', 'returnOnAssets', 'returnOnEquity', 'debtEquityRatio'])


