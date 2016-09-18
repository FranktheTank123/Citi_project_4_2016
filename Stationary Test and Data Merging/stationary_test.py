# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:41:02 2016

@author: linshanli
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
plt.ioff()

#helper functions
def my_plotting(name, date, data, wr, str_):
    plt.figure()
    plt.plot(date, data)
    plt.title(str_ + name)
    wr.savefig()     
    
def my_procedure_helper(name, date, data, plot, wr, er, str_):
    firm_i_adf = ts.adfuller(data)
    er.loc[i] = [name,firm_i_adf[0],firm_i_adf[1],(0 if firm_i_adf[1] <0.05 else 1)]    
    if(plot == 1):
        my_plotting(name, date, data, wr, str_)

##read in data
EXCEL = pd.read_csv("clearn_excess_roe_sp500v1.csv")
CLEAN = EXCEL[['Ticker', 'Quarter', 'Date', 'ROE', 'SP500ROE']]

##Generate list of firm
list_of_firm = EXCEL[['Ticker']].iloc[:,0]
list_of_firm = list_of_firm.unique() #list_of_firm is an array contains 505 tickers

#result holders
roe_pdf = PdfPages('roe_pdf.pdf')
ROE_RESULT = pd.DataFrame(columns=['Ticker', 'ADF_stat', 'ADF_pvalue', 'pass?'])
roe_d_pdf = PdfPages('roe_d_pdf.pdf')
ROE_d_RESULT = pd.DataFrame(columns=['Ticker', 'ADF_stat', 'ADF_pvalue', 'pass?'])
roe_e_pdf = PdfPages('roe_e_pdf.pdf')
ROE_e_RESULT = pd.DataFrame(columns=['Ticker', 'ADF_stat', 'ADF_pvalue', 'pass?'])
roe_e_d_pdf = PdfPages('roe_d_e_pdf.pdf')
ROE_e_d_RESULT = pd.DataFrame(columns=['Ticker', 'ADF_stat', 'ADF_pvalue', 'pass?'])

    
for i in range(len(list_of_firm)):
 
    firm_i_name = list_of_firm[i]
    firm_i = CLEAN[CLEAN['Ticker']==firm_i_name]
    
    firm_i_roe = np.transpose(np.array(firm_i[['ROE']]))[0]
    firm_i_roe_d = firm_i_roe[:-1] - firm_i_roe[1:]
    firm_i_roe_e = np.transpose(np.array(firm_i['ROE'] - firm_i['SP500ROE'].convert_objects(convert_numeric=True)))
    firm_i_roe_e_d = firm_i_roe_e[:-1] - firm_i_roe_e[1:]
    try: 
        firm_i_q = [datetime.strptime(x[0], '%m/%d/%y') for x in np.array(firm_i[['Date']])]
        my_procedure_helper(firm_i_name, firm_i_q, firm_i_roe, 1, roe_pdf, ROE_RESULT, 'ROE - ')
        my_procedure_helper(firm_i_name, firm_i_q[:-1], firm_i_roe_d, 1, roe_d_pdf, ROE_d_RESULT, 'ROE_difference - ')
        my_procedure_helper(firm_i_name, firm_i_q, firm_i_roe_e, 1, roe_e_pdf, ROE_e_RESULT, 'ROE_excess - ')
        my_procedure_helper(firm_i_name, firm_i_q[:-1], firm_i_roe_e_d, 1, roe_e_d_pdf, ROE_e_d_RESULT, 'ROE_excess_difference - ')
    except: 
        continue  


roe_pdf.close()
roe_d_pdf.close()
roe_e_pdf.close()
roe_e_d_pdf.close()

#export
roe_ex = pd.ExcelWriter('roe_p.xlsx', engine='xlsxwriter')
ROE_RESULT.to_excel(roe_ex)
roe_d_ex = pd.ExcelWriter('roe_d_p.xlsx', engine='xlsxwriter')
ROE_d_RESULT.to_excel(roe_d_ex)
roe_e_ex = pd.ExcelWriter('roe_e_p.xlsx', engine='xlsxwriter')
ROE_e_RESULT.to_excel(roe_e_ex)
roe_e_d_ex = pd.ExcelWriter('roe_e_d_p.xlsx', engine='xlsxwriter')
ROE_e_d_RESULT.to_excel(roe_e_d_ex)