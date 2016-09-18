# Stationary Test and Data Merging
This folder contains three important scripts:

* Stationarity_test.py
* statement_roe_combine_d2v.py
* statement_roe_combine_bow.py

## `Stationarity_test.py` 
### Description
For all of firms, checked the stationarity of ROE, the changes of ROE (`ROE_d`), excess ROE over the S&P500 (`ROE_e`), and the changes of excess ROE (`ROE_e_d`).

**Here are the key findings:**
* Generally speaking, most firm's ROE failed the ADF test for stationarity. (355/489 firms have p-value > 5%, failed the test. Recall that the null hypothesis of ADF test is the time-series has an unit root. Thus, the smaller the p-value, the more confidence to reject the null, and hence the time-series is stationary).
* After take the first differencing, most firm's changes in ROE passed the ADF test. (431/487 firms passed the test. We are missing two firms here because we loss one data point when taking the first differencing, and there is a minimum #observation requirement for python's ADF test).* Similar observations for excess ROE and the first difference for excess ROE.* The time-series plots provide strong visual effects. Indeed, ROE looks more like a random walk, whereas changes of ROE looks more stationary.

### Input

* `clean_excess_roe_sp500v1.csv`

This file conatinas ROE for each firm as well as S&P500 ROE. These data are extracted from Bloomberg terminal. This file was provided from **TBD** folder, and no change was further made before reading into Python.

###OutputThe output includes 4 excel files, which each contains the ADF test and p-value and whether the p-value is greater than 5%. The output also includes 4 pdf files, which each contains the time-series plots for `ROE`, `ROE_d`, `ROE_e`, `ROE_d_e` respectively for every firm.

###Key decision madeBased on this test, the team concluded ROEs in general are not stationary. Thus, instead of using previous level of ROE and predicting future level of ROE, the team now focus on predicting changes of ROE.

##`statement_roe_combine_d2v.py`###DescriptionThis procedure does two parts. The first part is to match ROE with SP500 ROE as well as lagged ROE, excess ROE and lagged excess ROE. It also does labeling such as quarter, top/bottom 33%.
The second part combine the output from the first part and the statement vector file. The algorithm matches the two using `key = ‘filename’`.###Input* **A statement vector file**. This file should contain the features that Doc2vec algorithm trained. The file name can be modified under the ‘parameter setup’ section of the code.* `Dates.csv` contains file name, cik and reporting date. Cik are the IDs for firms, collectively with reporting date, they pin down to one financial statement.* `Bloomberg ROE.xlsm` contains two tabs: ROE tab contains cik, dates and ROE for each of the firms. SPX tab contains dates and the corresponding SP500 ROE.###Output`DATES_with_ROE.csv` is the output from the first part.`‘final_’+’statement vector file name’.csv` is the output from the second part.##`statement_roe_combine_bow.py`###DescriptionThis procedure is essential the BOW version of the second part of the above algorithm. ###InputDATES_with_ROE.csv, which is the output of `statement_roe_combine_d2v.py`.
A statement vector file. This file should contain the features that BOW algorithm trained. The file name can be modified under the `parameter setup` section of the code.###Output `‘final_’+’statement vector file name’.csv`##N.B
The two algorithms above each finalized the data preprocess procedure. The outputs are then feed into GBT or RF algorithm for supervised learning and prediction of changes of ROE.

