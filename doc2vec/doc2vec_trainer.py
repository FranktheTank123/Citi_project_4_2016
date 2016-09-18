# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy and pandas
import numpy as np
import pandas as pd
# random
from random import shuffle

# parallelism
import multiprocessing

# file-path related
from os.path import join
import glob, os

##################### change this #############################
mypath = 'C:\\MFE_Citi\\CitiProject\\doc2vec_new' ## chagne this
model_name = 'statements_vectors.d2v'
target_vector_file_name = 'statement_vectors.csv'
new_model = False ## change to true is you don't have your model pre-trained
save_model = True ## we want to save the model for every epoch in case of crush

'''hyper parameters'''
'''
min_count:  ignore all words with total frequency lower than this.
            You have to set this to 1, since the sentence labels only appear once.
            Setting it any higher than 1 will miss out on the sentences.

window:     the maximum distance between the current and predicted word within a sentence.
            Word2Vec uses a skip-gram model, and this is simply the window size of the skip-gram model.

size:       dimensionality of the feature vectors in output. 100 is a good number.
            If you’re extreme, you can go up to around 400.

sample:     threshold for configuring which higher-frequency words are randomly downsampled

negative:   if > 0, negative sampling will be used,
            the int for negative specifies how many “noise words” should be drawn (usually between 5-20).

workers:    use this many worker threads to train the model
'''
start_alpha = 0.025
alpha_decrease_rate = 0.002
min_count = 1
window = 10
size = 100
sample = 1e-4
negative = 5
workers = multiprocessing.cpu_count()
epoches = 10
count_print = 5000 ## print every x many of files are dumped in

##################### change this #############################

class LabeledLineSentence(object):
    '''
    tailored class for this project, not touch, it's magic...
    sources is an array of txt file address to be read
    '''
    def __init__(self, sources):
        self.sources = sources

    def __iter__(self):
        count__ = 0

        for item_no, file_name in enumerate(self.sources):
            per_statement = []

            count__ += 1
            if not count__ % count_print:
                print ('now reading file #{}'.format(count__))

            for line in utils.smart_open(file_name):
                ## merge multiple lines in each docs into one statement (a list of words..)
                ## per_statement += utils.to_unicode(line).split()
                per_statement += utils.to_unicode(line).split() +['\n'] ## manually include line break
            yield LabeledSentence(per_statement, [os.path.basename(file_name)])

    def sentences_perm(self):
        shuffle(self.sources)
        #return self.sentences


## make the file path
files_path = join(mypath,'**/*.txt')
all_files = []
all_files_names = []

## extract all the .txt file paths and the file name
for filename in glob.iglob( files_path, recursive = True):
    all_files.append(filename)
    all_files_names.append(os.path.basename(filename))

## dump all files into the class
all_statements = LabeledLineSentence(all_files)

if new_model:
    ## initialize the model
    model = Doc2Vec(min_count=min_count, window=window, alpha=start_alpha, min_alpha=start_alpha# use fixed learning rate
                    , size= size, sample= sample, negative= negative, workers=workers
                    ,docvecs_mapfile = join(mypath,'mapfile.txt'))

    ## dump all the txt files into the model, which takes some time...
    model.build_vocab(all_statements)
else:
    model = Doc2Vec.load(join(mypath,model_name))



## we train the model X many times,
for epoch in range(epoches):
    print('epoch',epoch+1,'...')
    all_statements.sentences_perm() ## shuffle the order of the docs
    model.train(all_statements)
    model.alpha -= alpha_decrease_rate  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decays
    if save_model:
        model.save( join(mypath, model_name))
        model = Doc2Vec.load(join(mypath,model_name))


## retrieve the doc vectors one by one
statement_vectors = np.array([model.docvecs[x] for x in all_files_names])
print("Total achieved vector size: {}".format(statement_vectors.shape))

## save the csv
results = pd.DataFrame( statement_vectors )
results['all_files_names'] = all_files_names
cols = results.columns.tolist()
cols = cols[-1:] + cols[:-1] ## reorder the col
results = results[cols]
results.to_csv(join(mypath,target_vector_file_name), index =False )
