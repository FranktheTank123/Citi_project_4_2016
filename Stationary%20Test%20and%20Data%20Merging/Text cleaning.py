'''
coding environment Python 2.7
'''

import re
from bs4 import BeautifulSoup
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Parse files using regex
consequitivedots = re.compile(r'\.{2,}')
consequitivecom  = re.compile(r', ,')
stemmer = SnowballStemmer("english")

# Tokenize sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stopword = stopwords.words("english")
regex = re.compile("[^a-zA-Z-,.']")

# Local address for storing downloading raw text
raw_data = 'C:\\MFE_Citi\\CitiProject\\raw_txt\\missed_raw_text'
os.chdir(raw_data)

# Local Address for storing clean data
raw_data_clean = 'C:\\MFE_Citi\\CitiProject\\doc2vec_new\\clean_mising_file'


def clean_filing(filing_text):
    # Locate the <DOCUMENT> tag for extracting text
    start = filing_text.find("<DOCUMENT>")
    if start == -1:
        start = 0
    end = filing_text.find("</DOCUMENT>")
    if end == -1:
        end = len(filing_text)
    return  BeautifulSoup(filing_text[start:end]).get_text().encode().decode("ascii", "ignore")
    
def clean_str(string):
    # Escaping redundant punctuations after extracting text
    string = string.replace('\n',' ')
    string = re.sub(' +',' ',re.sub(', ,',' ',re.sub(' +',' ',regex.sub(' ',consequitivedots.sub(' ',re.sub('\t+',' ',re.sub('\n+',"\n",string)))))))
    
    string = string.lower()
    string = nltk.word_tokenize(string)
    sentences = [j for j in string if j not in stopword]
    if len(sentences) <= 5:
        return ''
    sentences = ' '.join(sentences)
    sentences = re.sub(',\.','.',re.sub(', ',' ',re.sub(' \.','. ',re.sub(',\. \.','.',re.sub('\.,','',re.sub(' ,',',',re.sub(' \. ','. ',re.sub(' -q',' 10-q',re.sub(' -k',' 10-k',re.sub(" '","'",re.sub(" 's","'s",sentences)))))))))))
    return sentences.strip()


for i in os.listdir(raw_data):
    if os.stat(i).st_size == 0:
        continue
    print ("Processing file", i)
    ticker = i[:i.find('_')]
    cik_num= i[i.find('_')+1:i.find('_',i.find('_')+1)]
    
    
    if not cik_num in os.listdir(raw_data_clean):
        os.makedirs(raw_data_clean+'\\'+str(cik_num))

        
    try:
        
        data = ''
        filing_text = open(raw_data+'\\'+i,'r').read()
        
        # Look for reporting period
        reading = filing_text[:1000].lower().split('\n')
        for item in reading:
            if item.find('period') >= 0:
                date = item.split('\t')[-1]
                break
        
            
            
        filing_text = clean_filing(filing_text)            
        token = tokenizer.tokenize(filing_text)
        token = [clean_str(i) for i in token if i.find('....')==-1 and i.find('----')==-1]
        token = [i for i in token if i != '']
        # decode('ISO-8859-1')
        
        filename = raw_data_clean+'\\'+ cik_num + "\\" + i[:i.find('.')] + "_" + date + '.txt'
        
        # read file and clean it
        print ("Cleaning %s" % filename)
        f_clean = open(filename, 'w')
        f_clean.write('\n'.join(token[1:]))
        f_clean.close()  
        
    except:
        pass
                












