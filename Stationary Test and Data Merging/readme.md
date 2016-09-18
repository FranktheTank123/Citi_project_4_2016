# Stationary Test and Data Merging
This folder contains three important scripts:

* Stationarity_test.py
* statement_roe_combine_d2v.py
* statement_roe_combine_bow.py

## `Stationarity_test.py` 
### Description
For all of firms, checked the stationarity of ROE, the changes of ROE (`ROE_d`), excess ROE over the S&P500 (`ROE_e`), and the changes of excess ROE (`ROE_e_d`).

**Here are the key findings:**

* After take the first differencing, most firm's changes in ROE passed the ADF test. (431/487 firms passed the test. We are missing two firms here because we loss one data point when taking the first differencing, and there is a minimum #observation requirement for python's ADF test).

### Input

* `clean_excess_roe_sp500v1.csv`

This file conatinas ROE for each firm as well as S&P500 ROE. These data are extracted from Bloomberg terminal. This file was provided from **TBD** folder, and no change was further made before reading into Python.

###Output

###Key decision made

##`statement_roe_combine_d2v.py`


The two algorithms above each finalized the data preprocess procedure. The outputs are then feed into GBT or RF algorithm for supervised learning and prediction of changes of ROE.
