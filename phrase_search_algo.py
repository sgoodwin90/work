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
import errno
import os, os.path
import requests
from collections import defaultdict
from datetime import date, datetime, timedelta


default_stdout = sys.stdout

startTime = datetime.now()

date_filter = input('Enter desired date period for all tickets after specified date(format: yyyy-mm-dd):')

key_phrase = input('Enter phrase to search for:')

#path = input('Enter path to dump text files:')

search_string = 'type:ticket created>' + date_filter

search_url = 'https://anki.zendesk.com/api/v2/search.json?query=' + search_string
user = 'sgoodwin@anki.com' + '/token'
pwd = 'wlekVMUjMxALMZTzZsf1F5liBGjR76FNsCx20tQZ'


#gather ticket list based on date filter input

search_response = requests.get(search_url, auth=(user, pwd))

search_data = search_response.json()

ticket_list = []

print('gathering ticket list...')

while search_url:
    search_response = requests.get(search_url, auth=(user, pwd))

    search_data = search_response.json()
  

    for field in search_data['results']:
        for k,v in field.items():
            if k == 'id':
                ticket_list.append(str(v))
    search_url = search_data['next_page']

    

# loop through desired ticket list and output comments as txt file for each ticket

print('gathering fields from ticket list...')


for x in ticket_list:

    url = 'https://anki.zendesk.com/api/v2/tickets/' + x + '/comments.json'
    user = 'sgoodwin@anki.com' + '/token'
    pwd = 'wlekVMUjMxALMZTzZsf1F5liBGjR76FNsCx20tQZ'

    response = requests.get(url, auth=(user, pwd))

    data = response.json()

    dict_list = []

    for comment in data['comments']:
        for k,v in comment.items():
            if k == 'id':
                comment_id = str(v)
            if k == 'body':
                comment = str(v)
            if k == 'created_at':
                created_date = str(v)

        dict_list.append(comment)
    
        
    with open(os.path.join('/Users/stuart/newcorpus/','ticket-' + str(x) + '.txt'),'w') as outfile:
        sys.stdout = outfile
        outfile.write("\n".join(dict_list))   

sys.stdout = default_stdout

def n_concordance_tokenised(text,phrase,left_margin=5,right_margin=5):
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


print("searching tickets for phrase...")

#file_path = '/Users/stuart/newcorpus/*.txt'   

sys.stdout = open("phrase_matches.txt", "w")

print('phrase searched:' + ' ' + str(key_phrase))

files = glob.glob('/Users/stuart/newcorpus/*.txt')
# iterate over the list getting each file 
for file in files:
   # open the file and then call .read() to get the text 
   with open(file) as f:
        text = f.read()
        tokens = word_tokenize(text)
        textList = Text(tokens)
        results = n_concordance_tokenised(textList, key_phrase)
        phrase_matches = len(results)
        if phrase_matches > 0:
            print(str(phrase_matches) + ' ' + 'phrase matches found in' + ' ' + str(file.split('/')[4].split('.')[0]))

sys.stdout = default_stdout

print("cleaning up text files...")

for f in files:
    os.remove(f)

print("script finished.")
print('total time =' + ' ' + str(datetime.now() - startTime))
