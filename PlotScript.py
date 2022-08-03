import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats

#import data
df = pd.read_excel('Sheets/data_final.xlsx')

naics = dict()

#Find matching industries
for index, row in df.iterrows():
    #add new code
    if str(row['NAICS Code'])[0:2] not in naics:
        naics[str(row['NAICS Code'])[0:2]] = [row['Ticker Symbol']]
    
    #check to make sure comp not already in dict
    added = False
    for key in naics:
        if row['Ticker Symbol'] in naics[key]:
            added = True
    
    if not added:
        naics[str(row['NAICS Code'])[0:2]].append(row['Ticker Symbol'])



###FIND WHICH SKILLS ARE IN HIGHEST DEMAND###
""" skills = {"No": 0, "Minor": 0, "Some": 0, "Major": 0, "Radical": 0}

for index, row in df2.iloc[8:].iterrows():
    r = df2.loc[[index]].at[index, "Q27"]
    if isinstance(r, str):
        word = r.split(" ")[0]
        if word in skills:
            skills[word] += 1


def getLists(dict):
    pre_nums = []
    for key in dict:
        pre_nums.append((key, dict[key]))
    #sort by value
    pre_nums.sort(key = lambda x: x[1], reverse=True)

    keys = []
    nums = []
    for tup in pre_nums:
        keys.append(tup[0])
        nums.append(tup[1])

    return (keys, nums)

df = pd.DataFrame({'Skills': getLists(skills)[0], 'val':getLists(skills)[1]})
# Figure Size
fig, ax = plt.subplots(figsize =(16, 9))
 
# Horizontal Bar Plot
ax.barh(getLists(skills)[0], getLists(skills)[1])
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)

# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
 
# Add Plot Title
ax.set_title('Belief in Change of Primary Business Activity Over Next 3 Years',
             loc ='left', )

plt.show() """



###CODE TO FIND MATCHES###
###THIS IS OLD###
""" for i in range(len(names1)):
    for j in range(len(names2)):
        if isinstance(names2[j], str):
            if names1[i].split(" ")[0] in names2[j].upper():
                print(names2[j].upper() , "Actual: ", names1[i]) """
    
company_names = ["AUTODESK", "AVERY DENNISON CORP", "BANK OF NEW YORK MELLON CORP", "BROOKFIELD ASSET MANAGEMENT", "COCA-COLA CO", "DXC TECHNOLOGY CO",
    "EASTGROUP PROPERTIES", "HASBRO INC", "HONDA MOTOR CO LTD", "JACOBS ENGINEERING GROUP INC", "NORDSTROM INC", "TEREX CORP", "UNILEVER PLC", "WALGREENS BOOTS ALLIANCE INC", 
    "WASHINGTON REIT", "ALLIANT ENERGY CORP", "MORGAN STANLEY", "MICROSOFT CORP", "SHELL PLC", "TELEFONICA SA", "WPP PLC", "ING GROEP NV", "ABBVIE INC", "OFS CAPITAL CORP",
    "BOISE CASCADE CO", "IQVIA HOLDINGS INC", "ALIBABA GROUP HLDG", "CISCO SYSTEMS INC", "HOLOGIC INC", "HCA HEALTHCARE INC", "AES CORP (THE)", "ZEBRA TECHNOLOGIES CP  -CL A", "ADVANSIX INC",
    "CREDIT SUISSE GROUP", "INCYTE CORP", "CI FINANCIAL CORP", "BRADESCO BANCO", "ACV AUCTIONS INC", "PAYSAFE LTD", "POWERSCHOOL HOLDINGS INC", "ARDAGH METAL PACKAGING SA",
    "RUSH ENTERPRISES INC", "SANOFI", "SAP SE", "AMKOR TECHNOLOGY INC", "COGNIZANT TECH SOLUTIONS", "GAIA INC", "CME GROUP INC", "WYNN RESORTS LTD", "AXIS CAPITAL HOLDINGS LTD",
    "POST HOLDINGS INC", "WESTERN UNION CO", "JAZZ PHARMACEUTICALS PLC", "VMWARE INC -CL A", "HORIZON THERAPEUTICS PUB LTD", "EPAM SYSTEMS INC", "GUIDEWIRE SOFTWARE INC",
    "WIPRO LTD", "ABB LTD", "INFOSYS LTD", "FRESENIUS MEDICAL CARE AG&CO", "ORANGE", "ICICI BANK LTD"]

#have to subtract 2 to get actual index
df1_company_ix = [2839, 1245, 271, 2325, 2477, 2577, 1921, 3495, 3117, 453, 1255, 1417, 3565, 2065, 1705, 393, 3267, 2315, 
    991, 3877, 2915, 3161, 1313, 361, 1797, 1087, 1891, 107, 2795, 151, 255, 3791, 1123, 3731, 3087, 1579, 1715, 1259, 2103,
    3345, 2241, 3421, 1771, 2829, 2163, 2005, 455, 3517, 2463, 1583, 3535, 3241, 187, 679, 3641, 1563, 909, 1349, 385, 3107, 3927]

""" matching_df1 = df1.head(0)
matching_df2 = df2.head(0)

for index, row in df1.iterrows():
    if row['Company.Name'] in company_names:
        matching_df1 = matching_df1.append(df1.iloc[[index]])

for index, row in df2.iterrows():
    if (index+2) in df1_company_ix:
        print(index)
        matching_df2 = matching_df2.append(df2.iloc[[index]])

matching_df1.index = range(0, len(matching_df1))
matching_df2.index = range(0, len(matching_df2))
 """

### SURVEY COMMUNICATON VS. ROA 2020 & 2019 ###
"""
Going to make a box plot with communication-focused
and not communication-focused during COVID and comparing ROA's in 2020
"""
""" lacked_comm_words = ["Not very important", "Slightly important", "Moderately important"]
improved_comm_words = ["Important", "Very important"]

lacked_comm = pd.DataFrame()
improved_comm = pd.DataFrame()

for index, row in matching_df1.iterrows():
    if index < 61:
        if matching_df2.iloc[[index]].at[index, "Q178_4"] in lacked_comm_words:
            lacked_comm = lacked_comm.append(pd.DataFrame([matching_df1.iloc[[index]].at[index, "ROA.2019...."]]))
            print("here")
        elif matching_df2.iloc[[index]].at[index, "Q178_4"] in improved_comm_words:
            improved_comm = improved_comm.append(pd.DataFrame([matching_df1.iloc[[index]].at[index, "ROA.2019...."]]))
        else:
            continue

lacked_comm.dropna(inplace=True)
improved_comm.dropna(inplace=True)

#Create plot
data = [lacked_comm.iloc[:, 0], improved_comm.iloc[:, 0]]
fig1, ax1 = plt.subplots()
ax1.set_title('Bringing in effective partners vs. 2019 ROA ')
plt.ylabel('ROA (%)')
ax1.boxplot(data)
plt.xticks([1, 2,], ['Non-effective', 'Effective'])
plt.show() """





###CODE FOR REGRESSION###

#Clean Data
""" ratio.dropna(inplace=True)

outlier_indices = []

for num in zip(np.abs(stats.zscore(ratio["Net Profit Margin"])), np.abs(stats.zscore(ratio["Net Profit Margin"]))):
    if num[0] > 3.5 or num[0] < 3.5:
        outlier_indices.append(num.index)

print(outlier_indices)



zscores_roa = np.abs(stats.zscore(ratio["Return on Assets"]))



#Present Data

def calc_range(x):
    return np.max(x) - np.min(x)

#Titles
plt.title("Net Profit Margin vs. Return on Assets (2017-2021)")
plt.xlabel('Net Profit Margin')
plt.ylabel('Return on Assets')
#Regression
m, b = np.polyfit(ratio["Net Profit Margin"], ratio["Return on Assets"], 1)
plt.plot(ratio["Net Profit Margin"], m*ratio["Net Profit Margin"]+b, label = f'y = {b} + {m}*x'.format('B0', 'B1'))

#Labels with Information Box
x_coord = ratio['Net Profit Margin'].max()
y_coord = ratio['Return on Assets'].max()
scale = calc_range(ratio.loc[:, "Return on Assets"])/60

plt.text(x_coord, y_coord - 4*scale, f'y = {m.round(4)}x + {b.round(4)}', horizontalalignment='right')

plt.text(x_coord, y_coord - 7*scale, f'Corr. = {round(np.corrcoef(ratio.loc[:, "Net Profit Margin"], ratio.loc[:, "Return on Assets"]).item(1), 5)}',horizontalalignment='right')

#Regression Line and Data
plt.scatter(ratio["Net Profit Margin"], ratio["Return on Assets"])
plt.text(x_coord, y_coord-scale, f'N = {len(ratio.index)}', horizontalalignment='right')

#Show
plt.show() """


