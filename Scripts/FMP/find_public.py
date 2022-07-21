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

    tickers = open('list_tickers.txt', 'r')

    #initialize dataset to be made
    dataPoints = ['symbol', 'date', 'currentRatio', 'quickRatio', 'cashRatio', 'netProfitMargin', 'returnOnAssets', 
        'returnOnEquity', 'debtEquityRatio']   

    df = pd.DataFrame(columns=dataPoints)


    def yearData(dict):
        """
        Takes in dictionary with possible dataPoints

        Returns a list with same n row dimension as DataFrame that we are trying to produce
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

    df.to_excel('data_fmp.xlsx')

sys.modules[__name__] = getRatio



