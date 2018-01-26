#!/usr/bin/env python

#parse_texts.py 
#
#by Joe Hahn
#jmh.datasciences@gmail.com
#24 January 2019
#
#this hack parses Gutenberg project books stored in data folder and extracts title, author, & content
#
#To execute:    ./parse_texts.py

#get list of files
import subprocess
files = subprocess.check_output(['find', 'iso', '-name', '*.txt']).decode('utf8').split('\n')[0:-1]
print 'approx number of books downloaded = ', len(files)

#this attempts to extract author & title from a sentence
def get_author_title(sentence):
    author = 'unclear'
    title = 'unclear'
    sentence_lc = sentence.lower()
    if ('gutenberg' in sentence_lc):
        gutenberg_split = sentence_lc.split('project gutenberg')
        if ('by' in gutenberg_split[1]):
            by_split = gutenberg_split[1].split('by')
            title = by_split[0]
            author = by_split[1]
        #some cleanup
        author = author.strip('.')
        author = author.strip(' ')
        author = author.strip('*')
        title = title.replace('etext of ', '').replace('etext ', '').strip(' ').strip(',')
        if (title[0:3] == "'s "):
            title = title[3:]
        author = author.title()
        title = title.title()
    return author, title

#loop over every file and extract title & author
import nltk
nltk.download(info_or_id='punkt')
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
import re
import random
sentences_list = []
for file in files:
    try:
        with open(file) as fp:
            raw_text = fp.read().decode('utf8').replace('\r\n', '|')
        print '===='
        print 'file = ', file
        if (raw_text[0] == '|'):
            raw_text = raw_text[1:]
        for j in range(len(raw_text)):
            if (raw_text[j] == '|'):
                break
        sentence = raw_text[0:j]
        print 'sentence =', sentence
        author, title = get_author_title(sentence)
        print 'author = ', author
        print ' title = ', title
        modified_text = raw_text.replace('|', ' ')
        sentences = nltk.sent_tokenize(modified_text)
        N_sentences = len(sentences)
        print 'N_sentences = ', N_sentences
        #drop first and last 15% of sentences that contain gutenberg boilerplate text
        middle_sentences = sentences[int(0.15*N_sentences) : int(0.85*N_sentences)]
        #preserve up 1000-3000 random sentences
        N_sentences = len(middle_sentences)
        if (N_sentences > 1000):
            if (N_sentences > 3000):
                N_sentences = 3000
        print 'preserving N_sentences = ', N_sentences
        random_sentences = random.sample(middle_sentences, N_sentences)
        for j in range(5):
            print 'sentence ' + str(j) + ' =' + random_sentences[j]
        for s in random_sentences:
            sentences_list += [{'input_file':file, 'author':author, 'title':title, 'sentence':s}]
    except:
        pass

#make dataframe of sentences
import pandas as pd
sentences = pd.DataFrame(sentences_list)
print '===='
print '===='
print 'number of parsed sentences = ', len(sentences)
print 'number of parsed books = ', len(sentences.groupby('input_file').count())

#save sentences
import pickle
with open('sentences.pkl', 'wb') as fp:
    pickle.dump(sentences, fp)
