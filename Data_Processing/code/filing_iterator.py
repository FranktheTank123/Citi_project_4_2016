import settings_new,  pickle, os, re
from bs4 import BeautifulSoup
from gensim.models import doc2vec
from nltk.corpus import stopwords
import pymysql

def clean_filing(filing_text):    
    """Cleans the filing text by stripping HTML"""    
    start = 0      
    doc_start_indices = [m.start() for m in re.finditer("<DOCUMENT>", filing_text)]
    
    for index in doc_start_indices:
        start = index
        break
    
    end = len(filing_text)
    doc_end_indices = [m.start() for m in re.finditer("</DOCUMENT>", filing_text)]    
    for index in doc_end_indices:
        end = index
        break
    
    return BeautifulSoup(filing_text[start:end]).get_text().lower().encode().decode("ascii", "ignore")

def filing_to_wordlist(filing_text):
    words = filing_text.split()
    return words

def filing_to_sentences(filing_text, tokenizer):    
    clean_text = clean_filing(filing_text)
    raw_sentences = tokenizer.tokenize(clean_text.strip())    
    sentences = []
    
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(filing_to_wordlist(raw_sentence))                
    return sentences

def get_filing_id(file_name, cik):
    txt_file_name = file_name.split(sep='/')[3].split(sep='.')[0]
    return str(cik) + '/' + txt_file_name

def get_words_from_doc(filing_text, tokenizer):
    clean_text = clean_filing(filing_text)
    raw_sentences = tokenizer.tokenize(clean_text.strip())            
    words = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            words += filing_to_wordlist(raw_sentence)
    
    return words

def get_words_from_doc_new(filing_text, tokenizer):
    #clean_text = clean_filing(filing_text)
    raw_sentences = tokenizer.tokenize(filing_text.strip())            
    words = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            words += filing_to_wordlist(raw_sentence)
    
    return words

def get_clean_text(filing_text):
    clean_text = clean_filing(filing_text)
    
    return clean_text

class filings_iterator(object):
    """Iterates through filings"""
    def __init__(self, tokenizer, year_start = 2000, year_end=2015,
                  file_sp500 = settings_new.BASE_PATH + settings_new.COMPANY_CIK_SP500,
                  useDB = False, N = 1, ticker = "DUMMY"):
        self.max_docs = N
        self.year_start = year_start
        self.year_end = year_end
        self.file_sp500 = file_sp500
        self.tokenizer = tokenizer
        self.useDB = useDB
        self.stops = set(stopwords.words("english"))
        self.file_list = []
        self.filing_id_list = []
        self.ticker = ticker
        self.file_list_new = []

        # check if we already have the list of files we want to process
        file_list_fname = settings_new.BASE_PATH_CLEAN_FILINGS_LIST+ '{}.pickle'.format("file_list")
        filing_id_list_fname = settings_new.BASE_PATH_CLEAN_FILINGS_LIST+ '{}.pickle'.format("filing_id_list")
        if (os.path.isfile(file_list_fname) and os.path.isfile(filing_id_list_fname)):
            with open(file_list_fname, 'rb') as f:
                self.file_list = pickle.load(f)
            with open(filing_id_list_fname, 'rb') as f:
                self.filing_id_list = pickle.load(f)
            print('Found pickle file {}, skipping DB check...'.format(file_list_fname))
            print('Found pickle file {}, skipping DB check...'.format(filing_id_list_fname))
            self.file_list_new = [x for x in self.file_list if (x.startswith(ticker+"_"))]
            print('length of file_list_new is:')
            print(len(self.file_list_new))
            print('length of file_list is:')
            print(len(self.file_list))
        else:
            # read list of S&P 500 companies
            f_sp500 = open(self.file_sp500)
            lines = f_sp500.readlines()    
            f_sp500.close()
            
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks', db='mfe_citi')  
            for line in lines:            
                fields = [field.strip() for field in line.split(sep = ',')]
                ticker = fields[1]
                company_cik = str(int(fields[2]))
                
                cur = conn.cursor()
                cur.execute('select f.cik, f.date_filed, f.form_type, f.file_name from filing_index f where f.form_type in(%s, %s) and f.cik = %s order by f.date_filed;',
                            ('10-K', '10-Q', company_cik, ))
                
                print('company cik is: '+company_cik)
        
                for record in cur:
                        date_filed = record[1]
                        form_type = record[2]
                        file_name = record[3]
                        
                        if (form_type in settings_new.FORM_TYPES and 
                            (int(float(date_filed[:4])) >= self.year_start and int(float(date_filed[:4])) <= self.year_end)):
                                            
                            # figure out filename
                            filename = '{}_{}_{}_{}.txt'.format(ticker, company_cik, form_type, str(date_filed))                       
                            self.file_list.append(filename)
                            self.filing_id_list.append(get_filing_id(file_name, str(int(company_cik))))
                        
                cur.close()
            conn.close()
            
            with open(file_list_fname, 'wb') as f:
                    pickle.dump(self.file_list, f)
            with open(filing_id_list_fname, 'wb') as f:
                    pickle.dump(self.filing_id_list, f)
        print('Populated {} filenames'.format(len(self.file_list)))    
    
    def get_filing_from_db(self):
        # read files from DB, clean them and create TaggedDocument
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks', db='mfe_citi')          
        words = []
        i = 0
        for i in range(0, self.max_docs):            
            pickle_file_name = settings_new.BASE_PATH_FILINGS + '{}.pickle'.format(self.file_list[i])
            if os.path.isfile(pickle_file_name):
                print('Found pickle file {}, skipping cleaning/tokenization...'.format(pickle_file_name))
                with open(pickle_file_name, 'rb') as f:
                    words = pickle.load(f)
            else:   
                cur = conn.cursor()
                cur.execute('select f.filing, f.date_filed from filings f where f.filing_id = %s',
                            (self.filing_id_list[i],))
                filing_text = ''                       
                for record in cur:
                    filing_text = record[0]
                cur.close()
                
                print('Cleaning {}...'.format(self.file_list[i]))
                words = get_words_from_doc(filing_text, self.tokenizer)
                
                with open(pickle_file_name, 'wb') as f:
                    pickle.dump(words, f)
                            
            yield(doc2vec.TaggedDocument(words = words, tags=[self.file_list[i]]))               
        conn.close()
        
    def get_filings_without_binary_content(self):
        # read files from DB, clean them and create TaggedDocument
        print("Getting filings content...")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks', db='mfe_citi')                  
        words = []
        i = 0
        print("Getting filings content...")
        for i in range(0, self.max_docs):
            
            pickle_file_name = settings_new.BASE_PATH_CLEAN_FILINGS + '{}.pickle'.format(self.file_list[i])
            if os.path.isfile(pickle_file_name):
                print('Found pickle file {}, skipping cleaning/tokenization...'.format(pickle_file_name))
                with open(pickle_file_name, 'rb') as f:
                    words = pickle.load(f)
            else:   
                cur = conn.cursor()
                cur.execute('select f.filing, f.date_filed from filings f where f.filing_id = %s',
                            (self.filing_id_list[i],))
                filing_text = ''                       
                for record in cur:
                    filing_text = record[0]
                cur.close()
                
                print('Cleaning {}...'.format(self.file_list[i]))
                words = get_words_from_doc(filing_text, self.tokenizer)
                
                with open(pickle_file_name, 'wb') as f:
                    pickle.dump(words, f)
                            
            yield(doc2vec.TaggedDocument(words = words, tags=[self.file_list[i]]))        
        conn.close()
    
    def get_filing_without_stopwords_from_db(self):
        # read files from DB, clean them and create TaggedDocument
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks', db='mfe_citi')         
        words = []
        i = 0
        if (self.max_docs > len(self.file_list_new)):
            self.max_docs = len(self.file_list_new)
        for i in range(0, self.max_docs):
            pickle_file_name = settings_new.BASE_PATH_FILINGS + '{}.pickle'.format(self.file_list_new[i])
            if os.path.isfile(pickle_file_name):
                print('Found pickle file {}, skipping cleaning/tokenization...'.format(pickle_file_name))
                with open(pickle_file_name, 'rb') as f:
                    words = pickle.load(f)
                    words = [x for x in words if (("1" not in x) and ("2" not in x) and ("3" not in x))]
                    words = [x for x in words if (("ly " in x) or (x.endswith("ly")))]
                    words = [x for x in words if (("july" not in x))]
            else:                 
                cur = conn.cursor()
                cur.execute('select f.filing, f.date_filed from filings f where f.filing_id = %s',
                            (self.filing_id_list[i],))
                filing_text = ''                       
                for record in cur:
                    filing_text = record[0]
                cur.close()
                
                print('Cleaning {}...'.format(self.file_list[i]))
                words = get_words_from_doc(filing_text, self.tokenizer)
                words = [x for x in words if (("1" not in x) and ("2" not in x) and ("3" not in x))]
                words = [x for x in words if (("ly " in x) or (x.endswith("ly")))]
                
                with open(pickle_file_name, 'wb') as f:
                    pickle.dump(words, f)
                            
            yield(" ".join([w for w in words if not w in self.stops]))
       
        conn.close()
            
    def get_all_filing_sentences_from_db(self):
        # read files from DB, clean them and create TaggedDocument
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='mfeadminsql', passwd='mferocks', db='mfe_citi')         
        
        i = 0
        sentences_to_return = []
        for i in range(0, self.max_docs):            
            pickle_file_name = settings_new.BASE_PATH_SENTENCES + '{}_sentences.pickle'.format(self.file_list[i])
            if os.path.isfile(pickle_file_name):
                print('Found pickle file {}, skipping cleaning/tokenization...'.format(pickle_file_name))
                with open(pickle_file_name, 'rb') as f:
                    sentences = pickle.load(f)
                    sentences_to_return = sentences_to_return + sentences
            else:   
                cur = conn.cursor()
                cur.execute('select f.filing, f.date_filed from filings f where f.filing_id = %s ', 
                            (self.filing_id_list[i],))
                filing_text = ''                       
                for record in cur:
                    filing_text = record[0]
                cur.close()
                
                print('Cleaning {}...'.format(self.file_list[i]))
                sentences = filing_to_sentences(filing_text, self.tokenizer)
                sentences_to_return = sentences_to_return + sentences
                
                with open(pickle_file_name, 'wb') as f:
                    pickle.dump(sentences, f)
        conn.close()
        return sentences_to_return
    
    def __iter__(self):
        return self.get_filings_without_binary_content()
        