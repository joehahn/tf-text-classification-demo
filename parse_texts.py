#parse_texts.py
#
#by Joe Hahn
#jmh.datasciences@gmail.com
#24 January 2019
#
#this parses Gutenberg project books stored in data, extracts the title and author
#when possible (succeeds about 33% of time)
#
#To execute:    python3 ./parse_texts.sh

#get list of files
import subprocess
files = subprocess.check_output(['find', 'data', '-name', '*.txt']).decode('utf8').split('\n')
print ('approx number of books downloaded= ' + str(len(files)))

#refresh storage directory
import os
os.system('rm -rf data/parsed; mkdir data/parsed')

#loop over every file and extract title & author...this requires python3
import nltk
nltk.download(info_or_id='punkt')
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
import pickle
books = []
for file in files:
    try:
        with open(file) as fp:
            raw_text = fp.read()
        print ('====')
        print ('file = ' + file)
        sentences = nltk.sent_tokenize(raw_text)
        N_sentences = len(sentences)
        print ('N_sentences = ' +  str(N_sentences))
        if (N_sentences > 1000):
            last_sentences = sentences[-5:]
            for s in last_sentences:
                if ('project gutenberg' in s.lower()):
                    s_split = s.split('by ')
                    author = s_split[-1].replace("\n", "").strip('.').replace('*', '')
                    author = author.replace('July 4th, 1994', ' ').replace("Second Series", " ")\
                        .replace('<toqyam@os.st.rim.or.jp>', ' ').replace('END OF PART III', ' ')\
                        .replace("PG has multiple editions of William Shakespeare's Complete Works", ' ')
                    author = author.strip(' ').strip(',')
                    title_str = s_split[:-1]
                    for t in title_str:
                        if ('project gutenberg' in t.lower()):
                            title = t.split('Project Gutenberg')[-1].replace('Etext', '')\
                                .replace('etext', '').replace('e-text of', '').replace('eText of', '')
                            title = title.replace("'s ", "").replace("*", "").replace("This  created", "")
                            title = title.replace('\n', '').strip('of ').strip(',').strip(' ')
                            title = title.replace("[#1 in our series is the Complete Works of Shakespeare,as presented to use", "")
                            title = title.replace("Edition of ", "")
                            #print ('s = ' + s)
                            print ('title = ' + title)
                            print ('author = ' + author)
                            middle_sentences = sentences[int(N_sentences/10) : int(0.9*N_sentences)]
                            N_sentences = len(middle_sentences)
                            d = {'input_file':file, 'author':author, 'title':title, 'N_sentences':N_sentences}
                            middle_sentences += [d]
                            out_file = 'data/parsed/' + author + '-' + title + '.pkl'
                            with open(out_file, 'wb') as fp:
                                pickle.dump(middle_sentences, fp)
                            books += [d]
                            break
    except:
        pass
print ('number of parsed books = ' + str(len(books)))

