# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 01:38:04 2018

@author: User
"""

import pandas as pd
import numpy as np

df = pd.read_csv('minWageData.csv')

#####convert education column to ordered numerics


#create a dictionary
clean = {'Typical education needed for entry': {"Doctoral or professional degree":13,
                                                "Master's degree":9.5,
                                                "Bachelor's degree":8,
                                                "Associate's degree":6,
                                                "Some college, no degree":7,
                                                "Postsecondary nondegree award":5,
                                                "High school diploma or equivalent":4,
                                                "No formal educational credential":0}}

df.replace(clean,inplace=True)

####take  logs of wage and minWage
df['log_Hourly_Wages']=np.log(df['H_MEAN'])
df['log_minWage']=np.log(df['minWage'])


###drop that weird column
df=df.drop(['Unnamed: 0'], axis = 1)



##group the states by years, so alabama will show up 12 times
d = {'State' : state, 'Year': year, 'minWage':minWage}

grouped = df.groupby('STATE')
df_main = pd.DataFrame(columns = ['State','Year','minWage'])
for state, group in grouped: #state is the name, group is a df
    groupedYear = group.groupby('Year')
    for year, groupYear in groupedYear:
        minWage = groupYear['minWage'].iloc[0]
        df_new = pd.DataFrame( {'State' : state, 'Year': year, 'minWage':minWage}, index = [0])
        df_main = df_main.append(df_new)

    
    year
    df = group[['
    #label the dataframes column with the states name and occ code
    df = df.rename(columns={'OCC_CODE': state +' '+ 'OCC_CODE'})
    #set the index to an index starting at 0
    df = df.reset_index(drop=True)
    df_main = pd.concat([df_main, df], axis = 1)

    
    
#data frame for all jobs among all YEARS
grouped = df.groupby('STATE')
df_main_year = pd.DataFrame()
for state, group in grouped:
    print(group)


df.to_csv('minWageDataUpdated.csv', encoding='utf-8', index=False)
df_main.to_csv('minWageDistributionData.csv', encoding='utf-8', index=False)

