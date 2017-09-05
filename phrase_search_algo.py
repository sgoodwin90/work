##phraseget

#SPECIAL NOTE: extracts and prints to screen part of sentnece using keyword
#Change keyword at bottom of code labled CHANGE KEYWORD

#instructions add texts to directory newcorpus on your desktop
#run this program-be patient
#results stored on desktop in output.txt


# kept adding these and they work dont ask details
# NOTE MUST install NLTK


from __future__ import division
import nltk, re, pprint, os
from nltk import sent_tokenize, word_tokenize
import os, fnmatch
from nltk.probability import FreqDist
from collections import Counter
import operator
from operator import itemgetter
import json
import csv
import sys
from nltk.text import Text
import glob
import shutil
import time


# First set the variable path to the directory path.  Use
# forward slashes (/), even on Windows.  Make sure you
# leave a trailing / at the end of this variable.

# Path for mac OS X will look something like this:
#text files from zendesk python api text algo script dump to home directory and need to be moved to below path
path = "/Users/Stuart/newcorpus/"


outfilename = 'newcorpus_condensed_' + str((int(time.time()))) + ".txt"


with open(outfilename, 'wb') as outfile:
    for filename in glob.glob('/Users/Stuart/newcorpus/*.txt'):
        if filename == outfilename:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)

           
            
#superkeywords = 'Cozmo'

text = open(outfilename, "r").read()
tokens = word_tokenize(text)
textList = Text(tokens)
#for word in superkeywords:
    #textList.concordance(word, 75, sys.maxsize)
#print(textList)
    
    
def n_concordance_tokenised(text,phrase,left_margin=5,right_margin=5):
    #concordance replication via https://simplypython.wordpress.com/2014/03/14/saving-output-of-nltk-text-concordance/
    phraseList=phrase.split(' ')
 
    c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
     
    #Find the offset for each token in the phrase
    offsets=[c.offsets(x) for x in phraseList]
    offsets_norm=[]
    #For each token in the phraselist, find the offsets and rebase them to the start of the phrase
    for i in range(len(phraseList)):
        offsets_norm.append([x-i for x in offsets[i]])
    #We have found the offset of a phrase if the rebased values intersect
    intersects=set(offsets_norm[0]).intersection(*offsets_norm[1:])
     
    concordance_txt = ([text.tokens[list(map(lambda x: x-left_margin if (x-left_margin) > 0 else 0,[offset]))[0]:offset+len(phraseList)+right_margin]
                        for offset in intersects])
                          
    outputs=[''.join([x+' ' for x in con_sub]) for con_sub in concordance_txt]
    return outputs
 

results = n_concordance_tokenised(textList, 'Customer Care')

keyword_matches = len(results)

print(str(keyword_matches) + ' ' + 'keyword matches found') 



---------------------

#stopwordcount

#instructions add texts to directory newcorpus on your desktop
#run this program-be patient
#results stored on desktop in output.txt


# kept adding these and they work dont ask details
# NOTE MUST install NLTK

from __future__ import division
import nltk, re, pprint, os
from nltk import sent_tokenize, word_tokenize
import os
from nltk.probability import FreqDist
from collections import Counter
import operator
from operator import itemgetter
import json
import csv
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '*']) # remove it if you need punctuation 



# First set the variable path to the directory path.  Use
# forward slashes (/), even on Windows.  Make sure you
# leave a trailing / at the end of this variable.

# Path for mac OS X will look something like this:
path = "/Users/Stuart/newcorpus/"


print("Starting")

           
corpus = []     # Empty corpus to hold corpus documents you put into newcorpus
emmadict={}     # Empty dictionary to hold word count key


# fd=nltk.FreqDist()
# Iterate through the corpus directory and build the corpus for NLTK.
listing = os.listdir(path) # start reading the files ino the corpus

for infile in listing:         #Can read single or multiple files saved in PLAIN TEXT-if it doesnt work file saved in wrong format 
    if infile.startswith('.'): #Mac directories ALWAYS have a .DS_Store file.
        continue               #This ignores it and other hidden files.
    url = path + infile        #this section gets the file names from the directory to read in
    f = open(url);
    raw = f.read()
    f.close()
    tokens = nltk.word_tokenize(raw)    #breaks up the text to single word=tokens
    tokenmain = [w for w in tokens if not w in stop_words]
    tokenlower = [w.lower() for w in tokenmain]
    corpus.append(tokenlower)               #puts the tokens in the corpus-a collection of you processed documents
    for w in tokenlower:                    #this goes through every word in corpus and counts them up and puts them in a dictionary format key, value pair
        if w in emmadict:
            emmadict[w] += 1
        else:
            emmadict[w] = 1
        
# prints out the results so you know its running                    
print("Prepared " + str(len(corpus)) + " documents...")
print("Still Running")


#reorders the key, values pair into descending order and store it in results

result = [(v, k) for k, v in emmadict.items()]
result.sort()
result.reverse()
result = [(k, v) for v, k in result]

print(result)


#store the key, value pair as comma seperated text in outout.txt
with open('stopoutput.txt','w') as f:
    wr = csv.writer(f)
    wr.writerows(result)

print('Finished')
