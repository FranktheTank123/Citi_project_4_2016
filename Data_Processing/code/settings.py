# date range
#START_YEAR = 1993
START_YEAR = 2000
END_YEAR = 2015

# Database connection string
#CONN_STRING = "host=127.0.0.1 dbname=mfe_citi user=mfe_citi_rw password=mfe123#"
#CONN_STRING = "host='127.0.0.1' user='mfe_citi_rw' password='mfe123#' db='mfe_citi'"
CONN_STRING = "host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks#', db='mfe_citi'"
#CONN_STRING = "host='127.0.0.1' port=3306 user='root' passwd='adminadmin' db='mfe_citi'"

#CONN_STRING = "host='127.0.0.1' port=3306 user='mfe_citi_rw' password='mfe123#' db='mfe_citi'"

#CONN_STRING = "user='mfe_citi_rw' password='mfe123#' host='127.0.0.1' database='mfe_citi'"


# data paths
# Windows
#BASE_PATH = "C:\\MFE_Citi\\CitiProject\\Jinyu\\R Code\\"
BASE_PATH = "C:\\MFE_Citi\\CitiProject\\R Code\\"
#BASE_PATH = "E:\\Books and Papers\\Citi_Seniority_Recovery\\R Code\\"
BASE_PATH_CLEAN_FILINGS = "C:\\MFE_Citi\\CitiProject\\clean_filings\\"
BASE_PATH_CLEAN_FILINGS_LIST = "C:\\MFE_Citi\\CitiProject\\clean_filings_list\\"
BASE_PATH_FILINGS = "C:\\MFE_Citi\\CitiProject\\filings\\"
BASE_PATH_SENTENCES = "C:\\MFE_Citi\\CitiProject\\doc2vec\\sentences_pickle\\"
BASE_PATH_FEATURES = "C:\\MFE_Citi\\CitiProject\\doc2vec\\features\\"
BASE_PATH_RAW_TXT = "C:\\MFE_Citi\\CitiProject\\raw_txt\\"
BASE_PATH_VECTORIZATION = "C:\\MFE_Citi\\CitiProject\\vectorization\\"

# Linux
#BASE_PATH = "/home/akshaym/E/Books and Papers/Citi_Seniority_Recovery/R Code/"
#BASE_PATH_CLEAN_FILINGS = "/media/akshaym/SSD/clean_filings/"
#BASE_PATH_FILINGS = "/media/akshaym/SSD/clean_filings/"
#BASE_PATH_FILINGS = "/home/akshaym/E/Books and Papers/Citi_Seniority_Recovery/Data/company_filings_data/"
#BASE_PATH_FILINGS = "/media/akshaym/Data2/SEC filings pickles/company_filings_data/"
#BASE_PATH_SENTENCES = "/media/akshaym/Data2/SEC filings pickles/company_filings_sentences/"
#BASE_PATH_FEATURES = "/media/akshaym/Data2/SEC filings pickles/company_filings_features/"

COMPANY_NAMES = "company_names.txt"
COMPANY_DEFAULT_DATES = "company_default_dates.csv"
COMPANY_CIK_NAMES_MAPPING = "company_names_cik_mapping.csv"
COMPANY_CIK_SP500 = "company_cik_sp500.csv"
COMPANY_CAPITAL_STRUCTURE = "company_capital_structure.csv"
DICTIONARY = "Oxford_English_Dictionary.txt"
DICTIONARY_ADJ = "adj.txt"

# SEC common form types
#FORM_TYPES = ['F-1', 'D', '3', '4', '5', 'S-1', '13D', '144', '20-F', 'ARS', '6-K', '10-Q', '10-K', '8-K']
#FORM_TYPES = ['424A', '424B1', '424B2', '424B3', '424B4', '424B5', '424B6', '424B7', '424B8', '10-Q', '10-K']
FORM_TYPES = ['10-Q', '10-K']
EDGAR_FTP_URL = "ftp://ftp.sec.gov/"
