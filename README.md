# Natural_Language_Processing
SE4395 NLP Course- Taken Fall 2022

## Overview of NLP

Click [here](/Overviews/NLP_Overview.pdf) to read a short overview of Natural Language Processing. 

## Text Classification

This [notebook](/text_classification/text_classify.pdf) takes a look at NLP models that classify textual data. A Kaggle dataset containing
almost 45,000 movie scripts and their genres was used. The baseline model is a sequential model which gets over 95% accuracy! 

## NLPete: Natural Language Processing Chatbot

NLPete is a natural language processing chatbot implemented in Python whose main goal is to successfully answer a user’s questions
on natural language processing topics. His two main components are a dictionary knowledge base and chat logic flow. The knowledge 
base is derived from Dr. Karen Mazidi’s book, Exploring NLP with Python: Building Understand Through Code, and NLPete’s chat logic 
parses user input and then queries the results from within this knowledge base using natural langauge processing techniques. While 
NLPete’s primary focus is the discussion of ideas related to understanding textual meaning, he also handles conversation outside of 
his domain quite well.   Read more [here](chatbot/Chatbot_paper_Kingsley_Yu.pdf).
 
Code for this project can be found [here](/chatbot/NLPete/)

Please put all files in the same folder and run main.py from the command line.

## Homework 1- Overview

Click [here](/Homework1/Homework1_KLK170230.py) to see the Python code for this assignment.

[Here](/Overviews/Homework1_overview.pdf) is a brief overview of homework 1.

## Homework 2- Exploring NLTK

Click [here](/Homework3/Assignment3_ExploringNLTK.pdf) to see the Notebook where the NLTK library is explored.


## Guessing Game

The [Guessing_game](/Guessing_game/main.py) is a program that uses the NLTK library and Python to create a word guessing 
game using an input file. First, the lexical diversity of the text file in calculated and some preprocessing is done.
Then, the game is created based on the long word tokens and nouns. Instructions can be viewed [here](/Guessing_game/instructions.pdf).
    
To run, put main.py and anat19.txt in the same folder and run: 
    
	python main.py anat19.txt   

## WordNet Notebook

This [notebook](/WordNet/WordNetNotebook.pdf) explores WordNet and SentiWordNet looking into synsets and and their sematnic relations.
Similarity is determined using the Wu-Palmer metric and Lesk algorithms, and collocation of bigrams is discussed.

## Ngrams

Ngrams are sliding windows of text that look at n words at a time. To read more on ngrams and language models, read the [narrative](/Ngrams/Ngrams_narrative.pdf).
     
This program consists of 2 parts. [Program 1](/Ngrams/ngrams_program1.py) which builds the ngram language model using 3 hardcoded data files in
different languages: English, Italian, and French. It creates pickles of unigram and bigram dictionaries for the 3 langauges as output. It can
be run by putting the 3 data files in the same folder as the program and typing:
  
	python ngrams_program1.py
   
[Program 2](/Ngrams/ngrams_program2.py) takes the pickled output of program 1 and uses the model created to test lines of an input file.
The model predicts the language of each line using conditional probabilities. Program 2 can be run using:
	  
	python ngrams_program2.py
 
The accuracy of our language model made using ngrams was 96.67%

## Webcrawler- Knowledge base

Web crawlers are programs that take a starting URL and jump from link to link extracting data. I created a web crawler that 
searches links for information related to Nessie: the monster of Loch Ness. The starting point for the crawler was the
Wikipedia page for Nessie found at https://en.wikipedia.org/wiki/Loch_Ness_Monster. The full doc can be found [here](/web_crawler/web_crawler.pdf).
  
The code to implement this crawler can be found by following this [link](/web_crawler/main.py). To run, navigate to the location
of the .py file and type:
 
	python main.py
 
This [folder](/web_crawler/) also contains a .db file that contains the Nessie knowledge base!

## Sentence Parsing

[Document](/Parsing/Sentence_parsing.pdf) where three different types of sentence parsing are explored: PSG, Dependency, and 
SRL. These parsers were used to break up the sentence-
 
On top of spaghetti all covered with cheese, I lost my poor meatball when somebody sneezed.
 
-and break it up based on structure, word relation, and semantics.

## Author Attribution

Google Colab [notebook](/AuthorAttribution/AuthorAttribution.pdf) where The Federalist Papers are used to explore sklearn
and machine learning models. First, the data is vectorized using TF-IDF vectorization, and then Bernoulli Naive Bayes, logistic
regression, and neural networks are used to try to predict author based on text. Surprisingly, Bernoulli Naive Bayes (with some
adjustments) was the best model!

## 2021 ACL Paper Summary

This [paper](/ACL/i_like_fish.pdf) summarizes the paper written for 2021 ACL conference titled "I like fish, especially dolphins: 
Addressing Contradictions in Dialogue Modeling". The paper talks about a new DECODE task written by interns and mentors
with the Facebook AI Research team. 


	