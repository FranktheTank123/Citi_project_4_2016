import PopulateDB, settings
import _thread
import threading
import time

year_start = 2000
year_end = 2015

def download_docs(threadName, threadNum):

    f = open(settings.BASE_PATH + settings.COMPANY_CIK_SP500)
    lines = f.readlines()    
    f.close()
    
    for line in lines:
        fields = [field.strip() for field in line.split(sep = ',')]
        ticker = fields[1]
        company_cik = str(int(fields[2]))
        PopulateDB.populate_filing_for_company(company_cik, ticker, True, '{}_{}'.format(ticker, company_cik), year_start, year_end)
    
def worker(fields, ticker, company_cik):
    """thread worker function"""
    PopulateDB.populate_filing_for_company(company_cik, ticker, True, '{}_{}'.format(ticker, company_cik), year_start, year_end)


f = open(settings.BASE_PATH + settings.COMPANY_CIK_SP500)
lines = f.readlines()    
f.close()

threads = []

count = 0    
for line in lines:
        if (count < 0):
            count +=1
            continue;
        count +=1
        print('line number: %s' % count)
        time.sleep(2)
        fields = [field.strip() for field in line.split(sep = ',')]
        ticker = fields[1]
        company_cik = str(int(fields[2]))
        if (count > 0):
            t = threading.Thread(target=worker, args=(fields, ticker, company_cik))
            threads.append(t)
            t.start()
            time.sleep(1)