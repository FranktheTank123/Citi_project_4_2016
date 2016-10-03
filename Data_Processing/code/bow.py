import settings_new, nltk.data, datetime, math
from filing_iterator_new import filings_iterator
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# some config parameters
year_start = 2000
year_end = 2015
num_features = 100
N = 28588 + 608 + 3
#N = 35000

# Get ticker
file_sp500 = settings_new.BASE_PATH + settings_new.COMPANY_CIK_SP500
f_sp500 = open(file_sp500)
lines = f_sp500.readlines()    
f_sp500.close()
             
for line in lines:            
    fields = [field.strip() for field in line.split(sep = ',')]
    ticker = fields[1]
    
    #ticker = "MSFT"

    # prepare training data
    docs = filings_iterator(tokenizer = nltk.data.load('tokenizers/punkt/english.pickle'), N = N, useDB = False, year_start = year_start, year_end = year_end,
                            ticker = ticker)
    
    # train bag-of-words model
    vectorizer = TfidfVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = num_features)
    
    train_data_features = vectorizer.fit_transform(docs.get_filing_without_stopwords_from_db())
    train_data_features = train_data_features.toarray()
    
    # write out bag of words to file
    f = open(settings_new.BASE_PATH + "BOW_FEATURES_{}.csv".format(ticker), 'w')
    
    
    # Write header
    f.write("Name,")
    f.write("CIK,")
    f.write("Date,")
    for i in range(1, num_features + 1):
        f.write("feat_{},".format(i))
    f.write("year.quarter")
    f.write("\n")
    
    # Sort Vectors
    feature_weight_sq = [0] * num_features
    N = len(train_data_features[:,0])
    for j in range(0, num_features):
        for i in range(0, N):
            feature_weight_sq[j]+=  train_data_features[i, j] ** 2
    feature_index = np.argsort(feature_weight_sq)
    
    # Create new vectors
    train_data_features_new = train_data_features
    for j in range(0, num_features):
        for i in range(0, N):
            train_data_features_new[i,j] = train_data_features[i,feature_index[j]]
    
    # Write data
    for i in range(0, N):
        rec = docs.file_list_new[i].split(sep='_')    
        document_features = train_data_features_new[i, :]
        f.write("{},".format(rec[0]))
        f.write("{},".format(rec[1]))
        date_str = rec[3][:-4]
        f.write("{},".format(date_str))
        for feature in document_features:
            f.write("{},".format(feature))
        filing_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")    
        f.write("{}-Q{}".format(filing_date.year, math.ceil(filing_date.month/3)))
        f.write("\n")
    f.close()
    
    f = open(settings_new.BASE_PATH + "FEATURE_NAMES_{}.csv".format(ticker), 'w')
    feature_names = vectorizer.get_feature_names()
    for j in range(0, num_features):
        f.write("{}\n".format(feature_names[feature_index[j]]))

    f.close()
