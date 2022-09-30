"""
    Name:   Kathryn Kingsley and Jonathan Yu
    UTID:   KLK170230
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the Ngrams pair assignment. It contains program 1.

"""
import pathlib  # for path
from nltk.tokenize import word_tokenize  # to tokenize raw text
from nltk.util import ngrams  # to use ngrams
import pickle  # for picklin'

'''
Get_tokens() is where most of the text processing occurs. 
First, the file is opened and read as raw text. All newlines
are removed and replaced with an empty string. The raw text 
is then tokenized. All the words are extracted and converted
to lower case in this step. The function takes a file argument 
and returns a list of tokens. 
'''


def get_tokens(file):
    # read all text from the file
    if file:
        with open(file, 'r', encoding='utf-8') as file:
            # remove new lines
            raw_text = file.read().replace('\n', '')
    else:
        print("Issue with opening file. Exiting program...")
        exit(1)
    # close the file
    file.close()
    tokens = [t for t in word_tokenize(raw_text)]
    # [t for t in word_tokenize(raw_text)]  # tokenize the raw text, stopwords? punctuation?
    # [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    return tokens


'''
Get_bigram_dictionary() is the function that creates the
dictionary of bigrams. Bigrams are all the combinations of
2 words in the corpus. This function takes tokens as an 
argument and returns a dictionary of bigrams where the 2 words
are the key and the number of occurrences of these 2 words in 
order is the value.
'''


def get_bigram_dictionary(tokens):
    bigrams = list(ngrams(tokens, 2))
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}
    return bigram_dict


'''
Get_unigram_dictionary() is the function that creates the
dictionary of unigrams. Unigrams are essentially tokens. The
function takes tokens as an argument and returns a dictionary 
of unigrams where the unigram is the key and the count is the
value.
'''


def get_unigram_dictionary(tokens):
    unigrams = list(ngrams(tokens, 1))
    uni_dict = {u: unigrams.count(u) for u in set(unigrams)}
    return uni_dict


'''
Get_dictionaries() is the function that forms the file path.
Tokens are created from the file, and then those tokens are 
given to 2 functions that returns a unigram dictionary and a 
bigram dictionary. It takes a filename as an argument and 
returns the 2 dictionaries.
'''


def get_dictionaries(filename):
    file = pathlib.Path.cwd().joinpath(filename)  # create path to file
    tokens = get_tokens(file)
    # print(tokens)
    uni_dict = get_unigram_dictionary(tokens)
    bi_dict = get_bigram_dictionary(tokens)
    return uni_dict, bi_dict


'''
Main() is the function where the unigram dictionary and the 
bigram dictionary for English, French, and Italian are created and pickled.
The function takes no arguments and returns no values.
'''


def main():
    # call get_dictionaries() once on each language file
    eng_uni_dict, eng_bi_dict = get_dictionaries("data/LangId.train.English")
    # french_uni_dict, french_bi_dict = get_dictionaries("data/LangId.train.French")
    # italian_uni_dict, italian_bi_dict = get_dictionaries("data/LangId.train.Italian")
    # pickle time
    pickle.dump(eng_uni_dict, open('uni_english_dict.p', 'wb'))
    #  pickle.dump(eng_uni_dict, eng_bi_dict, open('english_dicts.p', 'wb'))
    return


if __name__ == '__main__':
    main()
