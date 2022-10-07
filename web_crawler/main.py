"""
    Name:   Kathryn Kingsley
    UTID:   KLK170230
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the web crawler project. Some code inspired by
            Dr. Karen Mazidi's book:
            K. Mazidi, “13. Information Extraction,” in Exploring NLP  with Python: Building
            Understanding Through Code, First., 2019, p. 147 - 154.

"""
import os  # to make folders to keep things tidy
import pathlib  # to read the input file
from urllib import request  # to work with urls
from urllib.error import HTTPError  # to catch errors
import requests as requests
from bs4 import BeautifulSoup  # to work with html data
import re  # needed for regex in webcrawler
from nltk import sent_tokenize  # needed in clean_text
from nltk.corpus import stopwords
from nltk import word_tokenize
import math
import sqlite3  # for knowledge base

'''
The webcrawler() takes a starting link and extracts related
links from a page. It takes the starting URL as an argument
and returns a list of valuable links. It is called by main().
'''


def webcrawler(url):
    recrawl = 0
    # open the url and get in html format
    try:
        html = request.urlopen(url).read().decode('utf8')
    except HTTPError:
        print("Unable to open webpage. Exiting program...")
        exit(1)
    soup = BeautifulSoup(html, "html.parser")
    links = [url]
    # get at least 15 hyperlinks at the url
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        if url_check(link.get('href'), links):
            links.append(link.get('href'))
        if len(links) >= 18:
            return links
    recrawl -= 1
    webcrawler(links[recrawl])


'''
Url_check() filters out any potentially unwanted links using terms
I found to be impactful. It takes a url and a list of links as 
arguments and returns True or False depending on if the URL
is "good" or not.
'''


def url_check(url, links):
    # filter through the potential links
    wanted = ['ness', 'Ness', 'Nessie', 'nessie']
    unwanted = ['st-andrews', 'image', 'google', 'scotsman']
    if any(word in str(url) for word in wanted):
        if not any(word in str(url) for word in unwanted):
            if url not in links:
                return True
    return False


'''
The scrape_text function extracts text data from a webpage
in the form of paragraph headings in html format. It takes
a list of links as an argument and returns nothing. The 
output is a folder full of raw text files for a webpage.
It is called by main().  
'''


def scrape_text(links):
    file_number = 1
    for link in links:
        filename = 'raw_text/webpage_{}.txt'.format(file_number)
        file_number += 1
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        with open(filename, 'w', encoding='utf-8') as f:
            for p in soup.select('p'):
                f.write(p.get_text() + ' ')
        f.close()  # close that file
    return


'''
Clean_text() takes the raw text files and removes new lines
and unnecessary white spaces. It takes a list of links as 
an argument and returns nothing. Its output is a folder
of pages that are clean sentences for a given webpage.  
'''


def clean_text(links):
    file_number = 1
    for file in range(len(links)):
        text_file = 'raw_text/webpage_{}.txt'.format(file_number)
        sent_file = 'clean_sentences/sentences_{}.txt'.format(file_number)
        file_number += 1
        text = open(text_file, encoding='utf-8').read().strip()
        stripped = text.replace('\n', '').replace('\t', '')
        cleaned = re.sub(r'\[\d+]', '', stripped)
        cleaned = re.sub(r'\s\s\s+', '', cleaned)
        sentences = sent_tokenize(cleaned, 'english')
        with open(sent_file, 'a', encoding='utf-8') as f:  # open the file and write lines sentence by sentence
            for sentence in sentences:
                f.write(sentence + ' ')
        f.close()  # close that file
    return


'''
The function get_tf calculates the term frequency for 
a given file's context. It takes a file as an argument and returns 
a dictionary of TFs for the file. It is called by the 
get_important_terms function.
'''


def get_tf(file):
    tf_dict = {}
    stop_words = set(stopwords.words('english'))
    # lowercase and remove stop words
    tokens = [t for t in word_tokenize(open(file, encoding='utf-8').read().lower()) if
              t not in stop_words and t.isalpha()]
    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1
    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
    return tf_dict


'''
The function get_idf takes two arguments: the keys from one page
and the corpus-wide vocabulary. It determines the IDF for the 
entire corpus and returns it.
'''


def get_idf(vocab_by_topic, vocab):
    n = len(vocab_by_topic)
    idf_dict = {}
    for term in vocab:
        temp = ['x' for voc in vocab_by_topic if term in voc]  # count the number of docs the word occurs in
        idf_dict[term] = math.log((1 + n) / (1 + len(temp)))
    return idf_dict


'''
The function get_tf_idf takes two arguments: a dictionary of tfs
for one webpage and the corpus idf. It returns a dictionary of
TF_IDFs for the given webpage.
'''


def get_tf_idf(tf, idf):
    tf_idf_dict = {}
    for word in tf.keys():
        tf_idf_dict[word] = tf[word] * idf[word]
    return tf_idf_dict


'''
Get_important_terms() takes a list of links as an argument and prints
out TD-IDF most important terms. It returns nothing, but the printed
list is used to hard code the important words while creating the 
knowledge base. 
'''


def get_important_terms(links):
    file_number = 1
    tfs = []
    vocab_by_page = []
    vocab = []
    tf_idfs = []
    important_words = {}
    for file in range(len(links)):
        file = 'clean_sentences/sentences_{}.txt'.format(file_number)
        file_number += 1
        if os.stat(file).st_size > 0:
            tfs.append(get_tf(file))  # get tfs
    for file in tfs:
        vocab_by_page.append(file.keys())  # put all keys of a document in a dictionary separated by file
    for words in vocab_by_page:  # get a vocab for the corpus
        for word in words:
            if word not in vocab:
                vocab.append(word)
    idfs = get_idf(vocab_by_page, vocab)  # get idfs
    for i in range(0, len(tfs)):
        tf_idfs.append(get_tf_idf(tfs[i], idfs))
    for item in tf_idfs:  # get top 20 most important words from each file
        for word in sorted(item, key=item.get, reverse=True)[:20]:
            if word not in important_words:
                important_words[word] = item[word]
    for word in sorted(important_words, key=important_words.get, reverse=True)[:40]:  # print 40 most important words
        print(word, ': ', important_words[word])
    return


'''
Build_knowledge_base is where the knowledge base for Nessie is created.
It takes the number of files as an argument and returns nothing. It
starts by making a connection to a SQLite database and then creating
a table to store all of the facts. It then fills the table with sentences
containing the hardcoded important words. 
'''


def build_knowledge_base(number):
    # create database connection
    connection = sqlite3.connect('database.db')  # create db if it doesn't exist
    cur = connection.cursor()  # create cursor so I can interact with the knowledge base
    cur.execute('CREATE TABLE IF NOT EXISTS nessie (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT NOT NULL, '
                'context TEXT)')  # put the table schema in the db

    important_words = ['sightings', 'elusive', 'photographs', 'appearing', 'police', 'books', 'collection',
                       'nessie', 'day', 'since']
    for word in important_words:
        for i in range(number):
            file = 'clean_sentences/sentences_{}.txt'.format(i + 1)
            with open(file, 'r', encoding='utf-8') as f:  # open the file and write lines sentence by sentence
                text = f.read()
                sentences = [sentence.lower() for sentence in sent_tokenize(text)]
                for sentence in sentences:
                    if word in sentence:
                        cur.execute("INSERT INTO nessie (term, context) VALUES(?, ?)", (word, sentence))
                        connection.commit()
            f.close()
    # close db stuff
    cur.close()
    connection.close()
    return


'''
Main() is primarily a driver function. It takes no arguments and returns
nothing. It creates the directories for all the scraped and cleaned 
files and then calls the various functions to build the eventual 
knowledge base.
'''


def main():
    # make directories for all files
    parent_directory = pathlib.Path.cwd()
    if not os.path.exists('raw_text'):
        path = os.path.join(parent_directory, 'raw_text')
        os.mkdir(path)
    if not os.path.exists('clean_sentences'):
        path = os.path.join(parent_directory, 'clean_sentences')
        os.mkdir(path)
    url = 'https://en.wikipedia.org/wiki/Loch_Ness_Monster'  # root article
    links = webcrawler(url)
    num = len(links)
    scrape_text(links)
    clean_text(links)
    get_important_terms(links)
    build_knowledge_base(num)


if __name__ == '__main__':
    main()
