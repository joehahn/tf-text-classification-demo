#parse_texts.py 
#
#by Joe Hahn
#jmh.datasciences@gmail.com
#24 January 2019
#
#this hack parses Gutenberg project books stored in data folder and extracts title, author, & content
#
#To execute:    python ./parse_texts.py

#get list of files
import subprocess
files = subprocess.check_output(['find', 'iso', '-name', '*.txt']).decode('utf8').split('\n')[0:-1]
print 'approx number of books downloaded = ', len(files)

#this helper function is used below
def find_author(sentence):
    s_split = sentence.split('by ')
    author = s_split[-1].replace("\n", "").replace("\r", "").strip('.')
    author = author.replace('July 4th, 1994', ' ').replace("Second Series", " ")\
        .replace('<toqyam@os.st.rim.or.jp>', ' ').replace('END OF PART III', ' ')\
        .replace("PG has multiple editions of William Shakespeare's Complete Works", ' ')\
        .replace("Copyright laws are changing all over the world, be sure to check the copyright laws for your country before posting these files!!", ' ')
    author = author.replace('Copyright laws are changing all over the world, be sure to check the laws for your country before redistributing these files!!!', '')
    author = author.replace(', be sure to check the copyright laws for your country before posting these files!', ' ')
    author = author.replace('Copyright laws are changing all over the world', '')
    author = author.replace('Please take a look at the important information in this header', '')
    author = author.replace('in our series', '')
    author = author.replace(' in the PG catalog]', '')
    author = author.replace('Available as 7-bit version 7rbaa10', '')
    author = author.replace('[Volume II]', '')
    author = author.strip(' ').strip(',').strip(' ')
    author = author.strip(' ').strip(')').strip(' ')
    author = author.strip(' ').strip(']').strip(' ')
    author = author.strip(' ').strip('"').strip(' ')
    author = author.strip(' ').strip('.').strip(' ')
    author = author.strip(' ').strip('(coll').strip(' ')
    if ('Various' in author):
        author = 'Various'
    if ('Richard F. Burton' in author):
        author = 'Richard F. Burton'
    if ('Burroughs' in author):
        author = 'Burroughs'
    if ('Xenophon' in author):
        author = 'Xenophon'
    if ('Stephen Crane' in author):
        author = 'Stephen Crane'
    if ('L. Frank Baum' in author):
        author = 'L. Frank Baum'
    if ('Sherwood Anderson' in author):
        author = 'Sherwood Anderson'
    if ('Mark Twain' in author):
        author = 'Mark Twain'
    if ('Christopher Marlowe' in author):
        author = 'Christopher Marlowe'
    if ('Christoper Marlowe' in author):
        author = 'Christopher Marlowe'
    if ('Lord Dunsany' in author):
        author = 'Lord Dunsany'
    if ('William S. Gilbert' in author):
        author = 'William S. Gilbert'
    if ('Saxo Grammaticus' in author):
        author = 'Saxo Grammaticus'
    if ('Tokuya Matsumoto' in author):
        author = 'Tokuya Matsumoto'
    if ('Samuel Johnson' in author):
        author = 'Samuel Johnson'
    if ('Edmond Rostand' in author):
        author = 'Edmond Rostand'
    if ('Dumas' in author):
        author = 'Dumas'
    if ('Defoe' in author):
        author = 'Daniel Defoe'
    if ('John Martin Crawford' in author):
        author = 'John Martin Crawford'
    if ('Joseph Conrad' in author):
        author = 'Joseph Conrad'
    if ('Leo Tolstoy' in author):
        author = 'Leo Tolstoy'
    if ('Conan Doyle' in author):
        author = 'Author Conan Doyle'
    if ('Huxley' in author):
        author = 'Thomas H. Huxley'
    if ('James M. Barrie' in author):
        author = 'James M. Barrie'
    title_str = s_split[:-1]
    return author, title_str

#loop over every file and extract title & author
import nltk
nltk.download(info_or_id='punkt')
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
import re
import random
sentence_list = []
for file in files:
    try:
        with open(file) as fp:
            raw_text = fp.read()
        print '===='
        print 'file = ', file
        #drop accented characters by preserving alphanumerics plus simple punctuation 
        regex_str = '[^a-zA-Z0-9\n\.\,!\$\'`\"()#%&+-=:;<>{}\[\]]'
        filtered_text = re.sub(regex_str, ' ', raw_text.replace('\r\n', ' ')).replace('  ', ' ')
        sentences = nltk.sent_tokenize(filtered_text)
        N_sentences = len(sentences)
        if (N_sentences > 100):
            last_sentences = sentences[-5:]
            for s in last_sentences:
                if ('project gutenberg' in s.lower()):
                    if ('by ' in s.lower()):
                        author, title_str = find_author(s)
                    elif ('by ' in sentences[0].lower()):
                        author, title_str = find_author(sentences[0])
                    else:
                        author = 'Project Gutenberg'
                        title_str = [s]
                    for t in title_str:
                        if ('project gutenberg' in t.lower()):
                            title = t.split('Project Gutenberg')[-1].replace('Etext', '')\
                                .replace('etext', '').replace('e-text of', '').replace('eText of', '')
                            title = title.replace("'s ", "").replace("*", "").replace("This  created", "")
                            title = title.replace('\n', '').replace('\r', '').strip('of ').strip(',').strip(' ')
                            title = title.replace("[#1 in our series is the Complete Works of Shakespeare,as presented to use", "")
                            title = title.replace("Edition of ", "").replace('"', '')
                            title = title.replace('in our series', '')
                            title = title.replace('[There are many other eBooks', '')
                            title = title.replace('The One Volume Edition #12', '')
                            title = title.strip('EBook of ')
                            if ('Twenty Thousand Leagues Under the Sea' in title):
                                title = 'Twenty Thousand Leagues Under the Sea'
                            if ('ssay on Man' in title):
                                title = 'Essay on Man'
                            if ('lack Beauty' in title):
                                title = 'Black Beauty'
                            if ('ngland Under the Tudors' in title):
                                title = 'England Under the Tudors'
                            if ('The Lives Of The Twelve Caesars' in title):
                                title = 'The Lives Of The Twelve Caesars'
                            if ('leak House' in title):
                                title = 'leak House'
                            if ('Myths And Legends Of Our Own Land' in title):
                                title = 'Myths And Legends Of Our Own Land'
                            if ('The Tragical History of Dr. Faustus' in title):
                                title = 'The Tragical History of Dr. Faustus'
                            if ('Messer Marco Pol' in title):
                                title = 'Messer Marco Polo'
                            if ('The Count of Monte Crist' in title):
                                title = 'The Count of Monte Cristo'
                            if ('The Kalevala' in title):
                                title = 'The Kalevala'
                            if ('Dot and the Kangaroo' in title):
                                title = 'Dot and the Kangaroo'
                            if ('en-Hur: A Tale of the Christ' in title):
                                title = 'Ben-Hur: A Tale of the Christ'
                            if ('Sinking of the Titanic' in title):
                                title = 'Sinking of the Titanic'
                            if ('eauty and the Beast' in title):
                                title = 'Beauty and the Beast'
                            if ('ShakespeareFirst Folio/35 Plays' in title):
                                title = "Shakespeare's First Folio/35 Plays"
                                author = 'Shakespeare'
                            if ('The Memoirs of Napoleon' in title):
                                title = 'The Memoirs of Napoleon'
                                author = 'Louis Antoine Fauvelet de Bourrienne'
                            #print 's = ', s
                            print 'title = ', title
                            print 'author = ', author
                            #drop first 20% and last 10% of sentences, to avoid gutenberg boilerplate text
                            middle_sentences = sentences[int(N_sentences/10) : int(0.9*N_sentences)]
                            #preserve up to 3000 random sentences
                            N_sentences = len(middle_sentences)
                            if (N_sentences > 3000):
                                N_sentences = 3000
                            print 'N_sentences = ', N_sentences
                            random_sentences = random.sample(middle_sentences, N_sentences)
                            for s in random_sentences:
                                sentence_list += [{'input_file':file, 'author':author, 'title':title, 'sentence':s}]
    except:
        pass

#make dataframe of sentences
import pandas as pd
sentences = pd.DataFrame(sentence_list)
print 'number of parsed sentences = ', len(sentences)

#save sentences
import pickle
with open('sentences.pkl', 'wb') as fp:
    pickle.dump(sentences, fp)
