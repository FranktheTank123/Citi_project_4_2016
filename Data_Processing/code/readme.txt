This document provides an overview of the python programs used in data processing for Citi-Berkeley project.

Version: 2016.10.16

Main flow:

EDGARCrawler.py is used for downloading zip files of company filing index from ftp://ftp.sec.gov/edgar/

ExtractFiles.py is used for unzip the zip files

filing_iterator.py is used by bow.py to cleaned the raw documents by removing stopwords and unnecessary html tags (details could be referred to report)

get_company_filing.py is used to use the index results from ExtractFiles.py to download the company filings, i.e. 10K, 10Q documents of S&P 500 companies

PopulateDB.py is used by various python files to store the results (i.e. raw and cleanned files of company filings) on the hard disk or a mysql database.

bow.py is used for generating Bag of Words (BOW) vectors from cleanned documents.

Side flows:

Process_date.py is used to get the report date and filing date from the 10Q and 10K documents of the S&p 500 companies

process_dictionary.py is used to parse the Oxford dictionary into word + word class format.

settings_new.py is the class to store most of the static path