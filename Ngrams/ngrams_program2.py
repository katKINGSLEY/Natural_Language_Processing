"""
    Name:   Kathryn Kingsley and Jonathan Yu
    UTID:   KLK170230 and JCY180000
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the Ngrams pair assignment. It contains program 2.

"""

import pickle
from nltk import word_tokenize
from nltk.util import ngrams



#Dictionaries for easy term lookup
langs = ["eng", "french", "italian"]
names = ["English", "French", "Italian"]

        
def main():    
    # Read in pickle files and populate our lookup table
    lookup = {}
    for lang in langs:
        lookup[lang] = {}
        for gram in ["uni", "bi"]:
            lookup[lang][gram] = pickle.load(open(f"{lang}_{gram}_dict.p", "rb"))

    #Read in test data
    testData = open("data/LangId.test").readlines()
    solutions = open("data/LangId.sol").readlines()
    inaccuracies = [] #Table for storing the inaccurate lines

    for line in range(len(testData)):    
        #Calculate unigrams and bigrams    
        unigrams = word_tokenize(testData[line])
        bigrams = list(ngrams(unigrams, 2))
        #Initialize probability table
        p_laplace = [1,1,1]
        
        for bigram in bigrams:
            for i in range(3):     
                # For each language, multiply laplace table by the corresponding probability
                lang = langs[i]
                V = len(lookup[lang]["uni"])
                n = lookup[lang]["bi"][bigram] if bigram in lookup[lang]["bi"] else 0
                d = lookup[lang]["uni"][bigram[0]] if bigram[0] in lookup[lang]["uni"] else 0
                # Laplacian smoothing
                p_laplace[i] = p_laplace[i] * ((n+1)/(d+V))
        
        #Format result so we can compare it to our solutions array
        result = f"{line+1} {names[p_laplace.index(max(p_laplace))]}"

        if result != solutions[line].strip():
            inaccuracies.append(line)

    #Calculate # inaccurate then take complement
    acc = 1.0 - (1.0*len(inaccuracies)/len(testData))
    print("Accuracy: {0:.2%}".format(acc))
    print(f"Incorrect lines: {inaccuracies}")
main()    