# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 19:22:35 2018

@author: User
"""
import pandas as pd
import numpy as np 
import os

data_xls = pd.read_excel('state_M2015_dl.xlsx', index_col=None)
data_xls.to_csv('state2015.csv', encoding='utf-8', index=False)

starting_folder = ('ECON 480/data sets occupations/')
save_folder = ('Econ 480/')

for file in os.listdir(starting_folder):
    data_xls = pd.read_excel(file, index_col=None)
    output_name = save_folder + file + ".csv"
    data_xls.to_csv(output_name, encoding='utf-8', index=False)