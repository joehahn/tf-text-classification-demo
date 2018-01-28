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
        author = author.replace('etext', '').replace("'S", "'s").replace("complete", "")
        author = author.strip('.')
        author = author.strip(' ')
        author = author.strip('*')
        title = title.replace('ebook of ', '').replace('etext of ', '')\
            .replace('etext ', '').replace('ebook ', '').replace(',complete', '')\
            .replace(',entire', '').strip(' ').strip(',').strip('"')
        if (title[0:3] == "'s "):
            title = title[3:]
        author = author.title()
        title = title.title()
    return author, title

#loop over every file and extract title & author
import random
chunk_list = []
for file in files:
    try:
        with open(file) as fp:
            #raw_text = fp.read().decode('utf8')#.replace('\r\n', '|')
            raw_text = fp.read().replace('\r\n', '|')
        print '===='
        print 'file = ', file
        first_1000_chars = raw_text[0:1000].replace('\r\n', '|')
        if (first_1000_chars[0] == '|'):
            first_1000_chars = first_1000_chars[1:]
        for j in range(len(first_1000_chars)):
            if (first_1000_chars[j] == '|'):
                break
        sentence = first_1000_chars[0:j]
        #print 'sentence =', sentence
        author, title = get_author_title(sentence)
        print 'author = ', author
        print ' title = ', title
        modified_text = raw_text.replace('|', ' ')
        words = modified_text.split(' ')
        words = [word for word in modified_text.split(' ') if (word != '')]
        N_words = len(words)
        print 'N_words = ', N_words
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
        print 'N_chunks = ', len(text_chunks)
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

#apply some manual fixes to the some improperly parsed authors and titles
idx = chunks['author'].str.contains('Proudhon')
chunks.loc[idx, 'author'] = 'Proudhon'
idx = chunks['author'].str.contains('Homer')
chunks.loc[idx, 'author'] = 'Homer'
idx = chunks['author'].str.contains('Wake, Entire')
chunks.loc[idx, 'author'] = 'Archbishop Wake'
chunks.loc[idx, 'title'] = 'Forbidden Gospels and Epistles, Complete'
idx = chunks['title'].str.contains('War And Peace')
chunks.loc[idx, 'author'] = 'Leo Tolstoy'
idx = chunks['title'].str.contains('Nicholas Nickle')
chunks.loc[idx, 'title'] = 'Nicholas Nickleby'
chunks.loc[idx, 'author'] = 'Dickens'
idx = chunks['author'].str.contains('Dickens')
chunks.loc[idx, 'author'] = 'Dickens'
idx = chunks['author'].str.contains('Dick,')
chunks.loc[idx, 'title'] = 'Moby Dick'
chunks.loc[idx, 'author'] = 'Herman Melville'
idx = (chunks['author'] == 'Sshe')
chunks.loc[idx, 'author'] = 'Percy Bysshe Shelley'
chunks.loc[idx, 'title'] = 'The Complete Poetical Works of Percy Bysshe'
idx = chunks['author'].str.contains('Maupassant')
chunks.loc[idx, 'author'] = 'Maupassant'
idx = chunks['author'].str.contains('Dumas')
chunks.loc[idx, 'author'] = 'Dumas'
idx = chunks['author'].str.contains('Constant')
chunks.loc[idx, 'author'] = 'Constant'
idx = chunks['title'].str.contains('Supplemental Nights')
chunks.loc[idx, 'author'] = 'Sir Richard Francis Burton'
idx = chunks['title'].str.contains("Plutarch'S Lives")
chunks.loc[idx, 'title'] = "Plutarch's Lives"
idx = chunks['author'].str.contains("Xenophon")
chunks.loc[idx, 'author'] = "Xenophon"

#count number of chunks each book has, and cumulative sum
count = pd.DataFrame(chunks.groupby('input_file')['title'].count().sort_values())
count.columns = ['N_chunks']
count['N_chunks_cumulative'] = count['N_chunks'].cumsum()
count['N_chunks_cumulative'] /= count['N_chunks_cumulative'].max()
count = count.reset_index(level=0)
count.head()

#import plotting libraries
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
sns.set(font_scale=1.5, font='DejaVu Sans')

#plot cumulative sum of chunk counts...selecting books having 750 to 2200 chunks would capture
#the majority of books without causing serious class imbalance among the shorter books
#to view this plot,navigate to it using jupyter
fig, ax = plt.subplots(figsize=(12, 6))
xp = count['N_chunks']
yp = count['N_chunks_cumulative']
p = ax.plot(xp, yp, drawstyle='steps-mid')
p = ax.set_xlabel('number of chunks')
p = ax.set_ylabel('fraction of books')
p = ax.set_title('fraction of books having indicated number of chunks')
plt.savefig('figs/chunks.png')

#preserve records associated with books having 750+ chunks
chunks_counted = chunks.merge(count, on='input_file', how='inner')
idx = chunks_counted['N_chunks'] > 750
chunks_counted = chunks_counted[idx]
print 'number of records = ', len(chunks_counted)
chunks_counted.head()

#loop over each input_file and preserve random sample of each book's chunks, up to 2200 max
chunks_sampled = pd.DataFrame()
input_files = chunks_counted['input_file'].unique()
for input_file in input_files: 
    idx = (chunks_counted['input_file'] == input_file)
    df = chunks_counted[idx]
    Ns = len(df)
    if (Ns > 2200):
        df = df.sample(2200)
    chunks_sampled = chunks_sampled.append(df, ignore_index=True)
print 'number of records = ', len(chunks_sampled)
chunks_sampled.head()

#confirm that book contribute 750 to 2200 chunks
N_chunks = pd.DataFrame(chunks_sampled.groupby('input_file')['input_file'].count())
N_chunks.columns = ['N_chunks']
N_chunks = N_chunks.reset_index(level=0)
cols = [u'author', u'title', u'input_file', u'text_chunk']
chunks_recounted = chunks_sampled[cols].merge(N_chunks, on='input_file', how='inner')
cols = [u'author', u'title', u'input_file', 'N_chunks', u'text_chunk']
print chunks_recounted['N_chunks'].min(), chunks_recounted['N_chunks'].max()
print 'number of records = ', len(chunks_recounted)
chunks_recounted.head()

#for multi-book authors, drop all but the title having the most chunks, and add author_id
N = pd.DataFrame(chunks_recounted.groupby(['author', 'title', 'input_file'])['text_chunk'].count()).reset_index()
N = N.sort_values(['author', 'text_chunk'], ascending=False).drop_duplicates(['author'])
N = N.sort_values('author')
N = N.reset_index(drop=True)
N['author_id'] = N.index
print 'number of books = ', len(N)
N.head()

#join chunks_recounted to N to preserve the desired books, and randomize records
cols = ['author', 'author_id', 'title', 'input_file', 'text_chunk']
chunks_filtered = chunks_recounted.merge(N[['input_file', 'author_id']], on='input_file', how='inner')[cols]
chunks_filtered = chunks_filtered.sample(frac=1)[cols]
print 'number of records = ', len(chunks_filtered)
chunks_filtered.head()

#check the above 
N = pd.DataFrame(chunks_filtered.groupby(['author', 'title', 'input_file'])['text_chunk'].count())\
    .reset_index().sort_values('author')
N = N.rename(columns={'text_chunk':'N_chunks'})
print 'number of books = ', len(N)
N.head()

#save chunks
import pickle
with open('chunks.pkl', 'wb') as fp:
    pickle.dump(chunks_filtered, fp)
