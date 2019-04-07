# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:01:07 2018

@author: User
"""

import pandas as pd

##### goal: add the education requirements to each job in each state in each year
###### according to their occ code

educ = pd.read_csv('occupation education.csv')

wage = df.copy()

for occ in wage['OCC_CODE']:
    if occ = a value in educ(occ code):
       wage. append educ([education, experience, training ])
    else:
        wage. append ([na, na, na])

trial = wage[['STATE','Year','OCC_CODE']]

#note: trialList has to be <= to trial since each occ in trial corresponds
#to at most one code in educ

trialList = pd.DataFrame(columns = ['Typical education needed for entry',
       'Work experience in a related occupation',
       'Typical on-the-job training needed to attain competency in the occupation'])
for occ in trial['OCC_CODE']:
    flag = False
    for indx, name in enumerate(educ['code']):
        if occ == name:
            col1 = educ['Typical education needed for entry'][indx]
            col2 = educ['Work experience in a related occupation'][indx]
            col3 = educ['Typical on-the-job training needed to attain competency in the occupation'][indx]
            df = pd.DataFrame([[col1,col2,col3]], columns = ['Typical education needed for entry',
           'Work experience in a related occupation',
           'Typical on-the-job training needed to attain competency in the occupation'])
            trialList = pd.concat([trialList,df], ignore_index = True)
            flag = True
            break

    if not flag:
        col1=col2=col3 = "NaN"
        df = pd.DataFrame([[col1,col2,col3]], columns = ['Typical education needed for entry',
       'Work experience in a related occupation',
       'Typical on-the-job training needed to attain competency in the occupation'])
        trialList = pd.concat([trialList,df], ignore_index = True) 
    
dfnew = pd.DataFrame(columns = ['Typical education needed for entry',
       'Work experience in a related occupation',
       'Typical on-the-job training needed to attain competency in the occupation'])        

    ### holy fuck does this take long. write a fuckin sort algorithm ya knucklehead
    
#save trialList to .csv
trialList.to_csv('trialList.csv', encoding='utf-8', index=False)

#fidna a way to add two data frames of the same length

#merge trialList and wage 

trialcopy = trialList.copy()

trialcopy = pd.concat([wage,trialcopy], axis = 1)