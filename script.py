"""
Purpose of this script is to use Financial API services to provide full data coverage for the Harvey Nash dataset.
Will need to access all the ticker symbols for the companies listed in the HN dataset that currently intersects with the
dataset that Gio has provided

As a note a future data-entry position could be done to look through all entries in the HN dataset to provide ticker symbols
for the publicly traded companies in the survey. Then we would have a higher sampling quantity and be able to prove significance
more strongly (SOLVED re: ticker_webscraper)

v 1.0 (7/10/22):
    - Make a spreadsheet with company name, ticker symbol and useful financial information obtained from API
    - Using Selenium with Chromium webdriver to obtain ticker symbols from company names
    - Uses FMP (Financial Modeling Prep) API (250 requests/day) to obtain financial and balance statements for public companeis on HN Survey

v 1.1 (7/15/22):
    - Switched out FMP API for WRDS (Wharton) for financial data using Compustat
    - Cleaned ticker symbols so that there are no repeats
    - Obtained ratio data for kpi (key performance indicators)
        - Contained within Public_Company_Ratio_Data.xlsx
    - Cleaned ratio data (excluded missing data points/tickers with no data)

v 1.2 (7/21/22):
    - Accessed WRDS for ratios (beta) and used NAICS from fundamental query
    - Cleaned data (dropna)

v 1.2.0 (7/22-23/22):
    - Queried WRDS for industry standard data based on GICS sector codes 
    - Cleaned WRDS output for industry data
    - Looked for GICS codes for tickers using Fidelity.com and webscraping the sector names off the website
    - Wait for/Organized and cleaned GICS code results

v 1.2.1 (7/24/22):
    - Aggregating industry standard data time fit yearly time-series (instead of monthly)
        - industry_month_to_year
    - Need to fit data and put it against individual company data
        - Calculating % above industry standard for each company
        - Can make new spreadsheet with these %'s
    - Added __name__ == '__main__' functionality for module imports

v 1.2.2 (7/25/22):
    - Ran into some issues with querying datetime objects using sqlalchemy so had to convert datetime to regular strings in the industry year-series spreadsheet
    - Ran into issues with wrong dates/aggregation on the industry year-series so I had to mark when a year was ending and then dump previous year data
        - These issues are resolved now (.apply() function)

v 1.2.3 (7/27/22):
    - Began to graph regressions between financial ratios to make sure visualization code was complete
        -Error arose when outliers weren't being dealt with properly
    - Implemented 5% trim on all data entered to get rid of outliers
        - Outliers still aren't being processed

v 1.3 (7/29/22):
    - Data visualization complete and errors fixed 
        - Ran into indexing error and ended up ghaving to use dataframe instead of individual series to work
        - When dropping values from list, alters list and creates indexing problem essentially

v 1.3.1 (8/2/22):
    - Adding capabilities for box plots SOLVED
        - Have to scan and set-list to obtain possible answers for questions instead of having user-input those answers
        - O(n) time scale for this, shouldn't matter because of small N value (Takes like 5 seconds to query)

v 1.3.2 (8/12/22):
    - Touched up box plox implementation
        - Made sure plots did not show NaN values as answers
    - Created box_create_all function which goes through entire survey and works on box plots for all companies

All the implementation is finished for what is needed, survey qualitative analysis is now needed. Slight tweaking of code to account for variation in qualitative answers is now needed.
Can mass produce graphs and analyze for commonalities/scan them for interesting trends
"""
from cmath import isnan
import pandas as pd
import time
import random
import datetime
import fmpsdk
import os
import numpy as np
from scipy import stats 
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_public_fin_data(tickers, data_points, export_filename):
    """
    Parameters:
        - tickers: list of ticker names for companies that user needs data for
        - data_points: list of data points which represent financial data categories that they user needs data from
        - export_filename: filename that user wants to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Creates a 

    Notes:
        - Make sure you have .env file with API key
    """
    load_dotenv()
    apikey = os.environ.get("APIKEY")

    #initialize dataset to be made 
    df = pd.DataFrame(columns=data_points)

    def year_data(dict):
        """
        Parameters:
            - dict: Dictionary with possible data points (returned from fmpsdk)

        Actions:
            - list_vals : List of values associated with the keys specifed above
            - Goes through dictionary returned through sdk call and then cherry-picks categories for which the user needs data
        
        Notes:
            - None
        """
        list_vals = []

        for key in data_points:
            try:
                list_vals.append(dict[key])
            except:
                #if there isn't a datapoint for the certain ticker
                list_vals.append('None')
        return list_vals


    for ticker in tickers:
        try:
            for dict in fmpsdk.financial_ratios(apikey=apikey, symbol=ticker):
                #add row to dataframe
                df.loc[len(df.index)] = year_data(dict)
        except:
            #if fmpsdk doesn't have data for apikey (wastes one call unfortunately)
            continue

    df.to_excel(export_filename)

def ticker_webscraper(input_filename, company_col_name, export_filename):
    """
    Parameters:
        - data_xlsx: File path to the Harvey-Nash (HN) responses which contain respondent-input company names
        - company_col_name: String that represents the column in which users input their company name responses
        - export_filename: filename that you want to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Creates spreadsheet with a columns that have company names, ticker and the exchange on which the company is listed
    
    Notes:
        - Dependent on sleep, takes 2-10 seconds/query (random.random) * ~2000 companies = ~3.33 hours to complete (can probably bring this closer to ~1.5 hours)
            - Done to avoid google bot detector
        - Uses selenium module with chromium webdriver (or another webdriver of your choice)
            - Need these installed before you run function
        - Scraped from google.com stock view
    """

    df = pd.read_excel(input_filename)

    #columns 
    company_list = []
    ticker_list = []
    exchange_list = []

    driver = webdriver.Chrome()

    def company_url_converter(company):
        str = ''
        for word in company.split(' '):
            str += word
            str += '+'
        return str

    for index, row in df.iterrows():
        company = row[company_col_name]
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
    pd.DataFrame(data=d).to_excel(export_filename)

def gics_webscraper(input_filename, ticker_col_name, export_filename):
    """
    Parameters:
        - data_xlsx: File path to the spreadsheet that contains tickers 
        - company_col_name: String that represents the column name in which users input their ticker responses
        - export_filename: filename that you want to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Appends to existing spreadsheet a columns with the GICS sector code that relates to the ticker of the company queried from Fidelity.com (could use other source)

    Notes:
        - Fidelity has listings for 90% of publicly traded companies, could intersect different site outputs to obtain >90% coverage
        - Sleep is so fidelity.com doesn't think that we are webscraping 
        - Dependent on sleep, takes 2-5 seconds/query (random.random) * 168 companies = ~10 minutes to complete
    """

    df = pd.read_excel(input_filename)

    #need list for extra column
    #need dictionary for already queried sites (efficiency)
    gics_sector = []
    gics_dict = dict()

    driver = webdriver.Chrome()

    for index, row in df.iterrows():
        ticker = row[ticker_col_name]
        if ticker not in gics_dict:

            #query the fidelity website to obtain gics code
            driver.get(f'https://eresearch.fidelity.com/eresearch/evaluate/snapshot.jhtml?symbols={ticker}')
            try:
                info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr/td[4]/table[2]/tbody/tr/td[1]/div[3]/div[8]/span/a"))).text
            except:
                info = ' '
            
            #create new entry for gics sector
            print(f'{ticker} is under the {info} GICS sector')
            gics_dict[row['symbol']] = info
            gics_sector.append(info)

            #need to sleep so fidelity doesn't know it is a bot
            sleep = random.random()*3+2
            print("Sleeping for " + str(sleep))
            time.sleep(sleep)

        else:
            gics_sector.append(gics_dict[row[ticker]])
        
    #append to existing df, then export
    df['GICS Sector'] = gics_sector
    df.to_excel(export_filename)

def industry_month_to_year(input_filename, export_filename):

    """
    Parameters:
        - data_xlsx: File path to preadsheet that contains data that has the industry financial standards
        - date_col_name: String that contains the name of the column that has the date for the sector
        - export_filename: filename that you want to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Creates new spreadsheet which takes data from a monthly time series, aggregates then computes the mean, then applies that mean to the sector for that year
    
    Notes:
        - Creates list of dictionaries which is then turned into a pandas DataFrame object which is exported as an xlsx file
    """

    df = pd.read_excel(input_filename)

    def dict_average(dict):
        """
        Takes the average of value ints over the year time-series
        """
        for key in dict:
            if isinstance(dict[key], float):
                dict[key] = dict[key]/12
        return dict

    # Need dictionary for the year of data 
    # Logic flow: (sectors_year(dict) -> sector(dict, key) -> fin_data_category(dict, value, key) -> data_value(int, value))
    sectors_year = []
    sectors = {}

    for ix, row in df.iterrows():
        begin_year = False
        sector = ''
        fin_data = {}

        for col in row.index.tolist():
            if 'gic' in col.lower():
                sector = row[col]
            elif 'date' in col.lower():
                #need to dump at last entry of a year ('Utilities' is last entry for each month GICS)
                if df.iat[ix, 0].strftime("%m") == '12' and df.iat[ix, 1] == 'Utilities':
                    print("HERE")
                    begin_year = True
            fin_data[col] = row[col]
        
        #aggregate financial data from sheet
        sectors[sector] = {}
        for header in fin_data:
            try:
                sectors[sector][header] += fin_data[header]
            except:
                sectors[sector][header] = fin_data[header]
        
        #need to dump aggregate data from previous year if beginning of the year
        if begin_year:
            for header in sectors:
                print("added")
                sectors_year.append(dict_average(sectors[header]))
            sectors = {}

    new_df = pd.DataFrame(sectors_year)

    #change dates from datetime objects to MM/DD/YYYY so they are queriable
    new_df['Date'] = new_df['Date'].apply(lambda x: datetime.datetime.strftime(x, '%Y/%m/%d'))

    new_df.to_excel(export_filename)

def percent_to_industry(industry_filename, company_filename, export_filename):
    """
    Parameters:
        - industry_filename: File path to spreadsheet that represents the industry standard financial data
        - company_filename: File path to spreadsheet that represents company financial data
        - export_filename: filename that you want to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Creates spreadsheet that is similar to company_filename, but instead has percentages above industry standard for each data point in each financial category
    
    Notes:
        - Instead of looping through entire industry averages database, can use SQL to query into specific cells that we want
        - Can intersect the industry average and the company data to form a percentage above/below the industry and change the cell value of the existing company sheet 
            - Can change the headers to reflect the kind of statistical change you are making to end up with a new sheet
        - Not as easily replicable
            - Need to manually input years in which there are industry data
            - The renaming filters need user input as well
            - Can probably put these as parameters
    """
    company_df = pd.read_excel(company_filename)
    industry_df = pd.read_excel(industry_filename)

    #sql set up
    engine = create_engine('sqlite://', echo=False)
    industry_df.to_sql('industry', engine,if_exists='replace', index=False)

    #years with industry data
    year_data = ['2017', '2018', '2019', '2020', '2021']

    for i, row in company_df.iterrows():
        sector = row['GICS Sector']
        year = row['date'].split('-')[0]

        if year in year_data:
            #Query from data table the 
            result = engine.execute(f"Select * from industry where Date='{year}/12/31' and [GIC Description (Reference)]='{sector}'")
            ind_row = pd.DataFrame(result, columns=industry_df.columns)

            col_list = row.index.tolist()
            for j in range(len(col_list)):
                #check for number values
                col = col_list[j]
                if isinstance(row[col_list[j]], float):
                    company_df.iat[i, j] = ((company_df.iat[i, j]-ind_row.at[0, col])/abs(ind_row.at[0, col]))*100
    
    #change column names to represent data change
    new_col_names = []
    for col in company_df.columns:
        if 'date' in col.lower() or 'gics' in col.lower() or 'symbol' in col.lower():
            new_col_names.append(col)
        else:
            new_col_names.append("% Above/Below Industry Standard " + col)
        
    company_df.columns = new_col_names
    company_df.to_excel(export_filename)

def regression_visual(quant_filename, x_var, y_var, int_trim, export_filename):
    """
    Parameters:
        - quant_filename: File path to the spreadsheet with data for companies (raw or manipulated data)
        - x_var: string variable to be displayed on the x-axis (also the column name of the data)
        - y_var: string variable to be displayed on the y-axis (also the column name of the data)
        - int_trim: float value [0,1] that represents the proportion of data that will be trimmed to perform regression
        - export_filename: filename that you want to export it as (please include file preferred file type)
    
    Actions:
        - Returns: None
        - Makes a regression between two variables which demonstrates correlation between the two
    
    Notes:
        - Uses numpyplot and can add customization for graph as needed
        - Uses mean trim with 
    """
    
    company_df = pd.read_excel(quant_filename, index_col=0)

    def mean_trim_list(int_trim, df):
        """
        Parameters:
            - col: DataFrame column object
            - int_trim: Proportion of list 

        Actions:
            - Returns: list of indicies to delete from df
        """
        cut = int((len(df[x_var])*int_trim)/2)

        val_dict = {}
        #obtain sorted lists mapped to variable
        for var in [x_var, y_var]:
            listt = [(ix, row[var]) for ix, row in df.iterrows()]
            listt.sort(key= lambda x: x[1])
            val_dict[var] = listt
        
        #obtain index numbers from first and last cut for both and set ix_cut
        ix_cut = []
        for i in range(len(val_dict[x_var])):
            if (i < cut) or (i > len(val_dict[x_var]) - cut):
                ix_cut.append(val_dict[x_var][i][0])
                ix_cut.append(val_dict[y_var][i][0])
        
        #get rid of repeats
        return list(set(ix_cut))

    #drop spaces w/o data
    company_df[x_var].replace('', np.nan, inplace=True)
    company_df[y_var].replace('', np.nan, inplace=True)
    company_df.dropna(subset=[x_var,y_var], inplace=True)

    #obtain indices to drop and drop
    ix_cut = mean_trim_list(int_trim, company_df)
    company_df = company_df.drop(ix_cut)
    
    #Present Data
    def calc_range(x):
        return np.max(x) - np.min(x)

    #Titles
    plt.title(f"{x_var} vs. {y_var} (2017-2021)")
    plt.xlabel(f'{x_var}')
    plt.ylabel(f'{y_var}')
    
    #Regression
    company_df.dropna()
    m, b = np.polyfit(company_df[x_var], company_df[y_var], 1)
    plt.plot(company_df[x_var], m*company_df[x_var]+b, label = f'y = {b} + {m}*x'.format('B0', 'B1'))

    #Labels with Information Box
    x_coord = company_df[x_var].max()
    y_coord = company_df[y_var].max()
    scale = calc_range(company_df.loc[:, y_var])/60

    plt.text(x_coord, y_coord - 4*scale, f'y = {m.round(4)}x + {b.round(4)}', horizontalalignment='right')

    plt.text(x_coord, y_coord - 7*scale, f'Corr. = {round(np.corrcoef(company_df.loc[:, x_var], company_df.loc[:, y_var]).item(1), 5)}',horizontalalignment='right')

    #Regression Line and Data
    plt.scatter(company_df[x_var], company_df[y_var])
    plt.text(x_coord, y_coord-scale, f'N = {len(company_df.index)}', horizontalalignment='right')

    #Show and save
    plt.savefig(export_filename)

def box_visual(quant_filename, qual_filename, qual_var, int_trim):
    """
    Parameters:
        - quant_filename: File path to the spreadsheet with data for companies (raw or manipulated data)
        - qual_filename: File path to the spreadsheet with HN survey data
        - qual_variable: ID of question wanting to query
        - int_trim: Integer [0,1) that represents the amount of data needed to be trimmed from initial 
    
    Actions:
        - Returns: None
        - Makes box plot according to qualitiative categories on x-axis and value on the y-axis
    
    Notes:
        - Export filename is the combination of the unique question ID (ex. 'Q25') and the integer of the trim (in %)
    """
    quant_df = pd.read_excel(quant_filename, index_col=0)
    qual_df = pd.read_excel(qual_filename)
    
    def ticker_name_connection(df):
        """
        Parameters:
            - df: DataFrame that has tickers that correspond to the company names as listed on the survey

        Actions:
            - Returns dictionary mapping tickers to company names
        """
        name_dict = {}
        for _, row in df.iterrows():
            name_dict[row['Company Name']] = row['Ticker']
        return name_dict

    connect = ticker_name_connection(pd.read_excel('Sheets/tickers.xlsx'))
    plot_vals = {}

    #organize data into dictionary for plotting
    for _, row in qual_df.iterrows():
        if isinstance(row['Q45_2'], str):
            try:
                ticker = connect[row['Q45_2']]
                answer = row[qual_var]

                #check for nan values ( 'not isnan(answers)' doesn't work here for some reason )
                if isinstance(answer, str):
                    for ix, row in quant_df.iterrows():
                        if ticker == row['symbol']:
                            #KPI measurement
                            val = np.average(quant_df.iloc[ix, 4:9].tolist())
                            
                            if not isnan(val):
                                try:
                                    plot_vals[answer].append(val)
                                except:
                                    plot_vals[answer] = [val]
            except:
                continue
    
    def trim_outliers(dict):
        """
        Trims the dictionary lists to not include a proportion of the ends of the list
        """
        for key in dict:
            trim_num = int(len(dict[key])*int_trim/2)
            dict[key] = sorted(dict[key])
            dict[key] = [dict[key][i] for i in range(len(dict[key])) if i > trim_num and i < (len(dict[key]) - trim_num-1)]

    #trim and plot
    trim_outliers(plot_vals)
    data = [plot_vals[key] for key in plot_vals]
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    ax1.set_title('Category Rank vs. Average KPI Measure', fontsize=20) 
    plt.ylabel('Average KPI Measure Above Industry Average (%)', fontsize=12)
    #put x label on 2 lines to make readable
    x_label = qual_df.loc[1, qual_var].split(' ')
    x_label[int(len(x_label)/2)] += '\n'
    x_label = (' ').join(x_label)
    plt.xlabel(x_label, fontsize=12)
    ax1.boxplot(data)
    plt.xticks([(i+1) for i in range(len(plot_vals))], plot_vals)
    plt.savefig(f'Graphs/{qual_var}_{int(int_trim*100)}.png', dpi=300)

def box_create_all(quant_filename, qual_filename, int_trim):
    """
    Parameters:
        - quant_filename: File path to the spreadsheet with data for companies (raw or manipulated data)
        - qual_filename: File path to the spreadsheet with HN survey data
        - int_trim: Integer [0,1) that represents the amount of data needed to be trimmed from initial 
    """
    qual_df = pd.read_excel(qual_filename)

    #skip first 20 questions because of demographic questions
    for col in qual_df.columns[21:]:
        print(col)
        try:
            box_visual(quant_filename, qual_filename, col, int_trim)
        except:
            print("ERROR for ", col)
            continue

def regression_qual_vs_quant_visual(quant_filename, qual_filename, question_num, int_trim):
    """
    Goal is to go through all the filenames in the box plots and query the column of responses to determine correlation coefficient between certain answers
    For now can use dummy variables 1 and 0 for effective vs. ineffective at doing a certain task mentioned on the survey
    Can also do a difference of means calculation in order to find significant difference (Welch's T-Test since want to prove significance but the 2 samples don't have equal sizes)

    Output DataFrame will have different question names for rows and corresponding data analysis for columns
    """
    data_df = pd.read_excel(quant_filename, index_col=0)
    company_df = pd.read_excel(qual_filename, index_col=0)

    output_df = pd.DataFrame(columns=['Question', 'Difference of Means', 'Regression Model [y, m]', 'T-Test Significance (stat, p)', 'N-Value (Important, Not Important)'])

    for col in company_df.columns:
        dummy_vals = []
        important = []
        not_important = []
        if question_num in col:
            #Need to find company names which are in the percent_above_indsutry spreadsheet
            #tickers.xlsx map the company names to tickers
            #Need to use all data for this and say overall mean

            #Go down the company_df to obtain company names and values
            for _, row_data in data_df.iterrows():
                mean = np.mean([row_data['% Above/Below Industry Standard quickRatio'], row_data['% Above/Below Industry Standard currentRatio'],
                                row_data['% Above/Below Industry Standard netProfitMargin'], row_data['% Above/Below Industry Standard returnOnAssets'], 
                                row_data['% Above/Below Industry Standard returnOnEquity'], row_data['% Above/Below Industry Standard debtEquityRatio']])
                for _, row in company_df.loc[company_df['Q45_2'] == row_data['Company Name']].iterrows():
                    print(row[col])
                    if row[col] in ['Increase']:
                        if not isnan(mean):
                            important.append(mean)
                    elif row[col] in ['Decrease']:
                        if not isnan(mean):
                            not_important.append(mean)
            
            #Trim the important and non-important values
            int_cut_important = int((len(important)*int_trim)/2)
            int_cut_not = int((len(not_important)*int_trim)/2)
            important = sorted(important)
            not_important = sorted(not_important)
            important = [important[i] for i in range(len(important)) if int_cut_important < i < len(important)-int_cut_important]
            not_important = [not_important[i] for i in range(len(not_important)) if int_cut_not < i < len(not_important)-int_cut_not]

            dummy_vals = [1 for i in range(len(important))] + [0 for i in range(len(not_important))]
            
            output_df.loc[len(output_df.index)] = [col, np.nanmean(important)-np.nanmean(not_important), np.polyfit(dummy_vals, important + not_important, 1),
                stats.ttest_ind(important, not_important, equal_var=False), (len(important), len(not_important))]

    output_df.to_excel(f'Sheets/{question_num}.xlsx')
                             

if __name__ == "__main__":
    None


        
