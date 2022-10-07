# Natural_Language_Processing
SE4395 NLP Course- Taken Fall 2022

## Overview of NLP

Click [here](/Overviews/NLP_Overview.pdf) to read a short overview of Natural Language Processing. 


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

## Webcrawler- Knowledge base.

Web crawlers are programs that take a starting URL and jump from link to link extracting data. I created a web crawler that 
searches links for information related to Nessie: the monster of Loch Ness. The starting point for the crawler was the
Wikipedia page for Nessie found at https://en.wikipedia.org/wiki/Loch_Ness_Monster. The full doc can be found [here](/web_crawler/web_crawler.pdf).
  
The code to implement this crawler can be found by following this [link](/web_crawler/main.py). To run, navigate to the location
of the .py file and type:
 
	python main.py
 
This [folder](/web_crawler/) also contains a .db file that contains the Nessie knowledge base!

	