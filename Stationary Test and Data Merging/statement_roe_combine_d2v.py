'''
coding environment Python 3.4
'''
import numpy as np
import pandas as pd
import scipy.optimize as opt
from datetime import date, timedelta

### parameter setup
file_name = 'statement_vectors_300_final'
input_file_name = file_name+'.csv'
output_file_name = 'final_'+file_name ## this is csv format by defulat
t_lag = 3 ## this is how many lag data do we want to include in each fillings

### input data
## These tables are used in the first step and second step.
## DATES table contains file name, cik and reporting date. Cik are the IDs for firms, collectively with reporting date, 
## they pin down to one financial statement.
## ROE table contains cik, dates and ROE for each of the firms
## SPX table contains dates and the corresponding SP500 ROE
DATES = pd.read_csv('dates.csv')
ROE = pd.read_excel('Bloomberg ROE.xlsm', 'ROE')
SPX = pd.read_excel('Bloomberg ROE.xlsm', 'SPX')

##This table is used in the third step. It contains the word2vec trained vectors
Vectors =  pd.read_csv(input_file_name)

### customed helper functions
##This function labels roe baed on percentile. The top 1/3 labeled 1, the middle 2, the bottom 3, and the nan 4
##This function takes a list/array(in the format of PD series) and first calculate the top/bottom 1/3 barrier.
##Then assign 1-4 to the result dataframe. And output the dataframe.
def label_roe(group):
    results = group.copy() ## copy 
    
    ## get the top/bottom 1/3 barries
    bottom_ = np.percentile(group[group.notnull()],33)
    top_ = np.percentile(group[group.notnull()],66)
    
    results[group>=top_] = 1
    results[group<top_] = 2
    results[group<bottom_] = 3
    results[group.isnull()] = 4 ## 4 for NaN
    return results

##new functions to lable top 33% 1 in one column and bottom 33% 1 in another column
def label_roe_top(group):
    results = group.copy() ## copy 
    
    ## get the top 1/3 barries
    top_ = np.percentile(group[group.notnull()],66)
    
    results[group>=top_] = 1
    results[group<top_] = 0
    results[np.isnan(group)] = 0
    return results

def label_roe_bottom(group):
    results = group.copy() ## copy 
    
    ## get the bottom 1/3 barries
    bottom_ = np.percentile(group[group.notnull()],33)
    
    results[group<=bottom_] = 1
    results[group>bottom_] = 0
    results[np.isnan(group)] = 0
    return results
    
## These two functions are used to merge strings
def merge_str_ROE(s):
    return s[0]+s[1]+s[2]+s[3]
def merge_str_Vectors(s):
    return s[0]+s[1]+s[2]+s[3]+'.txt'
    
## clean the Date column in DATES
## Note that we are using report date as the date to match ROE
## A new column 'Date' is added. This is the column for doing further analysis
DATES['Date'] = pd.to_datetime(DATES['report_date'], format = '%Y%m%d')
## clean the cik column in ROE
## The following procedure added a new column cik, which changed CIK from string to integer
ROE['cik'] = [int(ROE['CIK'][x]) for x in range(len(ROE))]

### Step 1: Match firm's ROE and SP500 ROE
## Now use cik as the kwy to match between the DATES table and ROE table.
roe = [] #A temporary list contains ROEs matched 
for x in range(len(DATES)):
    try:
        ##first try to find exact date match. I.e. match cik and exactly match date
        roe.append(ROE[np.logical_and(ROE['cik'] == DATES['cik'][x],ROE['Date'] == DATES['Date'][x])]['ROE'].tolist()[0])
    except:
        ##Many times, dates are slightly off, in these cases look for dates that are within one month before
        i=1
        while(i<32):
            temp = ROE[np.logical_and(ROE['cik'] == DATES['cik'][x],ROE['Date'] == DATES['Date'][x]-timedelta(days=i))]['ROE'].tolist()
            if(not temp): ## temp is still empty, try another day before
                i+=1                
            else: ## we found it, can exist the loop early
                break
        if(not temp): ##after trying 32 days before, we still can't find this quarter's ROE, assign it as a nan value
            roe.append(float('nan'))
        else: ##else if found the ROE, use it.
            roe.append(temp[0])
DATES['ROE'] = roe #Now add roe as another column to the table DATES  
##see how many ROEs aren't found
#DATES[DATES.ROE.isnull()]
##Now match S&P500 ROE
##Exact same logic and procedure for matching firm's ROE. Detailed comment see above.
SProe = []
for x in range(len(DATES)):
    try:
        SProe.append(SPX[SPX['Date'] == DATES['Date'][x]]['ROE'].tolist()[0])
    except:
        i=1
        while(i<8):
            temp = SPX[SPX['Date'] == DATES['Date'][x]-timedelta(days=i)]['ROE'].tolist()
            if(not temp):
                i+=1                
            else:
                break
        if(not temp):
            SProe.append(float('nan'))
        else:
            SProe.append(temp[0])
DATES['SP500_ROE'] = SProe 
## Note all SP500 ROE found within 8 days off
#Calculate excess ROE
DATES['excess_ROE'] = DATES['ROE']-DATES['SP500_ROE']

##sort DATES table according to date
DATES = DATES.sort(['ticker', 'Date'])

##Finally add index
DATES.index = range(0,len(DATES))

## Calculate changes of ROE
## Note that if a nan value is present, a nan value is assigned. 
ROE_change = [float('nan')]
for x in np.arange(1,len(DATES)):
    if (DATES['cik'][x] != DATES['cik'][x-1]): #For first date, a nan value is always assigned 
        ROE_change.append(float('nan'))
    else:
        ROE_change.append(DATES['ROE'][x]-DATES['ROE'][x-1])
DATES['ROE_change'] = ROE_change  

## Calculate of changes of excess ROE, exactly procedure as above for changes of ROE
Excess_change = [float('nan')]
for x in np.arange(1,len(DATES)):
    if (DATES['cik'][x] != DATES['cik'][x-1]):
        Excess_change.append(float('nan'))
    else:
        Excess_change.append(DATES['excess_ROE'][x]-DATES['excess_ROE'][x-1])
DATES['ROE_excess_change'] = Excess_change  

## function to add N lags to any dataframe file
def add_t_k (N, file):
    ## N is number of lags, N >= 1
    ## file is an Dataframe table that to be add columns to
    ## Now find t-k value for the four columns: ROE, excess ROE, changes of ROE, changes of exces ROE
    for k in np.arange(1,N+1):
        ROE_t_k = k*[float('nan')]
        excess_ROE_t_k = k*[float('nan')]
        ROE_change_t_k = k*[float('nan')]
        ROE_excess_change_t_k = k*[float('nan')]
        for x in np.arange(k,len(DATES)):
            if (DATES['cik'][x] != DATES['cik'][x-k]):
                ROE_t_k.append(float('nan'))
                excess_ROE_t_k.append(float('nan'))
                ROE_change_t_k.append(float('nan'))
                ROE_excess_change_t_k.append(float('nan'))
            else:
                ROE_t_k.append(DATES['ROE'][x-k])
                excess_ROE_t_k.append(DATES['excess_ROE'][x-k])
                ROE_change_t_k.append(DATES['ROE_change'][x-k])
                ROE_excess_change_t_k.append(DATES['ROE_excess_change'][x-k])

        file['ROE_t-'+str(k)] = ROE_t_k
        file['excess_ROE_t-'+str(k)] = excess_ROE_t_k
        file['ROE_change_t-'+str(k)] = ROE_change_t_k
        file['ROE_excess_change_t-'+str(k)] = ROE_excess_change_t_k
    return file
DATES = add_t_k (t_lag, DATES)

#switch orders of columns
'''
DATES = DATES[['filename', 'report_date', 'filing_date', 'ticker', 'cik', 'SP500_ROE', 'Date', \
               'ROE', 'excess_ROE', 'ROE_change', 'ROE_excess_change', 'ROE_t-1', 'excess_ROE_t-1', 'ROE_change_t-1', 'ROE_excess_change_t-1']]
'''

### Step 2: labelling according to percentile within each quarter
## Calculate quarters and insert a column in the format of yyyy.q
DATES['Quarter'] = ["{}.{}".format(DATES['Date'][x].year, DATES['Date'][x].quarter) for x in range(0,len(DATES))]

##rank the ROE, into 3 groups and insert a column of label into the table
##1 means top 33%, 2 means middle 33%, 3 means bottom 33%, 4 are the nan values
DATES['Label'] = DATES.groupby(['Quarter']).ROE.apply(label_roe)

## New label: lable 1 for top 33% in one column and bottom 33# in another column
DATES['Label_top'],DATES['Label_bottom'] = DATES.groupby(['Quarter']).ROE.apply(label_roe_top), \
DATES.groupby(['Quarter']).ROE.apply(label_roe_bottom)
quarter = [x[-1] for x in DATES['Quarter']]
def quarter_ind(q):
    if q == '1':
        return '1000'
    elif q == '2':
        return '0100'
    elif q == '3':
        return '0010'
    else:
        return '0001'
temp = list(map(quarter_ind,quarter))

DATES['is_q1'] = [x[0] for x in temp]
DATES['is_q2'] = [x[1] for x in temp]
DATES['is_q3'] = [x[2] for x in temp]
DATES['is_q4'] = [x[3] for x in temp]

DATES.to_csv('DATES_with_ROE.csv')

### Step3: Match ROE table with word2vec vectors
## Now want to match between the two tables. Want to use file name as the key, but need to do a bit more work to create
## a new column 'match_file_name' for each table and they'll be exact match
## Split the string for file name column for the DATES table and Vector table
Vectors_file_name_splitted = Vectors['all_files_names'].apply(str.split, sep='_')
ROE_file_name_splitted = DATES['filename'].apply(str.split, sep='_')

## Re-append the strings together, but using customarized helper functions
Vectors['match_file_name'] = Vectors_file_name_splitted.apply(merge_str_Vectors)
DATES['match_file_name']= ROE_file_name_splitted.apply(merge_str_ROE)

## Now match using 'match_file_name' columns. Final is the resulting table.
final = Vectors.merge(DATES, left_on = 'match_file_name', right_on = 'match_file_name')

## Drop the unnecessary columns
final.drop(['match_file_name','filename', 'Unnamed: 5'], axis=1, inplace=True)

##Done! output as a CSV
final.to_csv(output_file_name + '.csv')

'''
## Output a cleaned version without the nan
final_cleaned = final[final['ROE_change_t-1'].notnull()]
final_cleaned.to_csv( output_file_name +'_cleaned.csv')    
'''