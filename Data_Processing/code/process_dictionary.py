import settings, re, math, logging, nltk.data, os

file_dic = settings.BASE_PATH_VECTORIZATION + settings.DICTIONARY
f_dic = open(file_dic, encoding="latin-1")
lines = f_dic.readlines()    
f_dic.close()
            
for line in lines:
    if ((' adv.' in line) and 'ly adv.' not in line):
        k = line.split(' ') 
    
    if ((' adj.' in line) and ' n.' not in line):
        k = line.split(' ')   
        if ('latin' in line or 'italian' in line):
            print(k[0]+' '+k[1])
        else:
            print(k[0])    