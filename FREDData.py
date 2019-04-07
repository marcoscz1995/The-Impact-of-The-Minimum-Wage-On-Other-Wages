# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:31:58 2018

@author: User
"""
import pandas as pd

##### get min wage data from the FRED
from fredapi import Fred
fred = Fred(api_key='09c96bb35bc2459c2ac9e444ebdd1575')
data = fred.get_series('STTMINWGMA')

stateAbrev = pd.read_csv('stateminwages.csv')
#make a new data frame with state names and abreviations
stateAbrev = stateAbrev[['Name','State Abbreviation']].copy()

#make a list with the state abreviations
unique_list = []
for x in stateAbrev['State Abbreviation']:
    if x not in unique_list:
            unique_list.append(x)
st = unique_list

#make a list with the state names
unique_list1 = []
for x in stateAbrev['Name']:
    if x not in unique_list1:
            unique_list1.append(x)
stateName = unique_list1          
            
# make a list by combining all the state abreviations to the fred name
fred_list = []
for st in st:
    fred_name = 'STTMINWG'+st
    fred_list.append(fred_name)

#convert to data frames and concat
fred_list = pd.DataFrame({'State Abbreviation':fred_list})
stateName = pd.DataFrame({'State Name':stateName})
fred_list = pd.concat([fred_list, stateName], axis = 1)

    ######
    # not all states have min wage data from the fred. in those cases
    #you will need to skip them and then later use the federal minimum wage
    #in their place
    #put a continue thing in this for loop
    
#make dataframe from the fred and combine them
minWageData = pd.DataFrame()    
for indx, name in enumerate(fred_list['State Abbreviation']): # ie name  = STTMINWGAK
    try:
        
        data = fred.get_series_all_releases(name) #download the data
        #change the date to year format and remove the old columns
        data['date'] = pd.to_datetime(data['date']) 
        data['Year'] = data['date'].dt.year
        data.drop(columns = ['realtime_start'], inplace = True, axis =1)
        data.drop(columns = ['date'], inplace = True, axis =1)
        #label the columns with min wage and year
        data.columns = ['Minimum Wage', 'Year']
        #label each datafram by its state name
        state_name = fred_list['State Name'][indx]
        data["State"] = data.shape[0]*[state_name]
        # add each new dataframe to the right
        minWageData = minWageData.append(data)
        
    except Exception: #if an error arrises from a file not available in the fred
        #use the federal min wage instead
        data = fred.get_series_all_releases('STTMINWGFG')
        data['date'] = pd.to_datetime(data['date']) 
        data['Year'] = data['date'].dt.year
        data.drop(columns = ['realtime_start'], inplace = True, axis =1)
        data.drop(columns = ['date'], inplace = True, axis =1)
        data.columns = ['Minimum Wage', 'Year']
        state_name = fred_list['State Name'][indx]
        data["State"] = data.shape[0]*[state_name]
        # add each new dataframe to the right
        minWageData = minWageData.append(data)
        
############ make all the data go from 2002-2017

df = minWageData.copy()
df = df[df['Year']>2001]   #keeps everything that is greater than 2001
df = df[df['Year']<2018]    
        
 ########## 
#check which states do not have only 16 years of min wage data
#this is a helper method
for indx, name in enumerate(df['State']):
    g = df.groupby(['State'])
    state1 = g.get_group(name)
    stateLength = len(state1)
    if stateLength != 16:
        print(name, stateLength)

# note that arizona, florida, oregon, mayland,minesota data
# either start at weird dates or have multiple min wage hikes so we remove them
df = df[df['State'] != 'Arizona']
df = df[df['State'] != 'Florida']
df = df[df['State'] != 'Oregon']
df = df[df['State'] != 'Minnesota']
df = df[df['State'] != 'Maryland']



## add the federal min wage column


data = fred.get_series_all_releases('STTMINWGFG')
data['date'] = pd.to_datetime(data['date']) 
data['Year'] = data['date'].dt.year
data.drop(columns = ['realtime_start'], inplace = True, axis =1)
data.drop(columns = ['date'], inplace = True, axis =1)
data.columns = ['Federal Minimum Wage', 'Year']
data = data[data['Year']>2001]   #keeps everything that is greater than 2001
data = data[data['Year']<2018]

fedWage = data[['Federal Minimum Wage']] #this returns a dataframe whereas
#fedWage = data['Minimum Wage'] returns a series

####### add the fedwage to df

#add a new empty column where the fed min wage will be added

#this is a list filled with repeating values of fedWage
i = 0
df1 = pd.DataFrame()
while i < 720:
    df1 = df1.append(fedWage)
    i+=16

repeatFedWage = df1.copy()
minWageData = df


repeatFedWage.to_csv('repeatFedWage.csv',encoding='utf-8', index=False)
minWageData.to_csv('minWageData.csv',encoding='utf-8', index=False)


# i added the two dfs in excel