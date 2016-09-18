'''
coding environment Python 3.4
'''
import numpy as np
import pandas as pd
import scipy.optimize as opt
from datetime import date, timedelta

### parameter setup
file_name = 'BOW_FEATURES_ADV_v6'
input_file_name = file_name+'.csv'
output_file_name = 'final_'+file_name ## this is csv format by defulat

### input data
## These tables are used in the first step and second step.
## DATES table contains file name, cik and reporting date. Cik are the IDs for firms, collectively with reporting date, 
## they pin down to one financial statement.
## ROE table contains cik, dates and ROE for each of the firms
## SPX table contains dates and the corresponding SP500 ROE
DATES = pd.read_csv('dates.csv')

##This table is used in the third step. It contains the word2vec trained vectors
Vectors =  pd.read_csv(input_file_name)

## format key
DATES['Date'] = pd.to_datetime(DATES['filing_date'], format = '%Y%m%d')
Vectors['Date_new'] = pd.to_datetime(DATES['Date'], format = '%m/%d/%y')
DATES['key']= [str(DATES['cik'][x])+str(DATES['Date'][x]) for x in range(len(DATES))]
Vectors['key']= [str(Vectors['CIK'][x])+str(Vectors['Date_new'][x]) for x in range(len(Vectors))]

## Match
Vector_file = Vectors.merge(DATES, left_on = 'key', right_on = 'key')

ROE = pd.read_csv("DATES_with_ROE.csv")

final = Vector_file.merge(ROE, left_on = 'filename', right_on = 'filename')

final.drop(['Unnamed: 5_x', 'Unnamed: 0','Date_new','key','report_date_y', 'filing_date_y', 'ticker_y', 'cik_y','Unnamed: 5_y',], axis = 1, inplace = True)

##Done! output as a CSV
final.to_csv(output_file_name + '.csv')

'''
## Output a cleaned version without the nan
final_cleaned = final[final['ROE_change_t-1'].notnull()]
final_cleaned.to_csv( output_file_name +'_cleaned.csv')
'''