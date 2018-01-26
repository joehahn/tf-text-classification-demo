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

#size (in words) of each chunk of text
chunk_size = 100

#this attempts to extract author & title from a sentence
def get_author_title(sentence):
    author = 'Unclear'
    title = 'Unclear'
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
        title = title.replace('ebook of ', '').replace('etext of ', '').replace('etext ', '').strip(' ').strip(',')
        if (title[0:3] == "'s "):
            title = title[3:]
        #some manual tweaks
        if ('Proudhon' in author):
            author = 'Proudhon'
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
chunk_list = []
for file in files:
    try:
        with open(file) as fp:
            raw_text = fp.read().decode('utf8')#.replace('\r\n', '|')
        print '===='
        print 'file = ', file
        first_1000_chars = raw_text[0:1000].replace('\r\n', '|')
        if (first_1000_chars[0] == '|'):
            first_1000_chars = first_1000_chars[1:]
        for j in range(len(first_1000_chars)):
            if (first_1000_chars[j] == '|'):
                break
        sentence = first_1000_chars[0:j]
        print 'sentence =', sentence
        author, title = get_author_title(sentence)
        print 'author = ', author
        print ' title = ', title
        modified_text = raw_text.replace('\r\n', ' ')
        words = nltk.word_tokenize(modified_text)
        N_words = len(words)
        #print 'N_words = ', N_words
        #drop first and last 15% of sentences that contain gutenberg boilerplate text
        middle_words = words[int(0.15*N_words) : int(0.85*N_words)]
        N_words = len(middle_words)
        text_chunks = []
        for j in range(0, N_words, chunk_size):
            chunk_of_words_list = middle_words[j:j+chunk_size]
            chunk_of_words_str = ''
            for word in chunk_of_words_list:
                chunk_of_words_str += word + ' '
            text_chunks += [chunk_of_words_str]
        print 'number of text_chunks = ', len(text_chunks)
        #insert each chunk into a dict containing author, title, file, chunk etc
        for text_chunk in text_chunks:
            chunk_list += [{'input_file':file, 'author':author, 'title':title, 'text_chunk':text_chunk}]
    except:
        pass

#make dataframe of sentences
import pandas as pd
cols = ['author', 'title', 'input_file', 'text_chunk']
chunks = pd.DataFrame(chunk_list)[cols]
idx = (chunks['author'] != 'Unclear') & (chunks['title'] != 'Unclear')
chunks = chunks[idx]
print '===='
print '===='
print 'number of parsed chunks of text = ', len(chunks)
print 'number of parsed books = ', len(chunks.groupby('input_file').count())

#save sentences
import pickle
with open('chunks.pkl', 'wb') as fp:
    pickle.dump(chunks, fp)
