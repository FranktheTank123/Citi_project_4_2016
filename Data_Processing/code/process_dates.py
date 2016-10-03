import os
import settings as s

f = open(s.BASE_PATH + "dates.csv", "w")

# Write header
f.write("filename,")
f.write("report_date,")
f.write("filing_date,")
f.write("ticker,")
f.write("cik,")
f.write("\n")

for filename in os.listdir(s.BASE_PATH_RAW_TXT):

    myfile = filename
    f.write("{},".format(myfile))
    
    file = open(s.BASE_PATH_RAW_TXT+filename)
    lines = file.readlines()    
    file.close()            
    for line in lines:            
        if ("CONFORMED PERIOD OF REPORT:" in line):
            report_date = line[-9:].replace(" ","").replace("\n","")
        if ("FILED AS OF DATE:" in line):
            filing_date = line[-9:].replace(" ","").replace("\n","")            
    print (filename.replace(".txt",""))

    ticker = filename.split('_',2)[0]
    cik =  filename.split('_',2)[1]  
    

    f.write("{},".format(report_date))
    f.write("{},".format(filing_date))
    f.write("{},".format(ticker))
    f.write("{},".format(cik))    
    f.write("\n")
    
f.close()
