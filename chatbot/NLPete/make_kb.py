import PyPDF2
import pickle
import spacy
import string
import re
import yake
from nltk import sent_tokenize
from nltk.corpus import stopwords

blacklist = [". . . . . . . ", "Section", "Chapter", "http:", "https"]
stop_words = stopwords.words("english")
nlp = spacy.load("en_core_web_md")

def is_sentence(text):
	# Check if text is a sentence. A sentence has two nouns and one verb.
	sent = nlp(text)
	if sent[0].is_title and sent[-1].is_punct:
		nouns = 2
		verbs = 1
		for token in sent:
			if token.pos_ in ["NOUN", "PROPN", "PRON"]:
				nouns -= 1
			elif token.pos_ == "VERB":
				verbs -= 1
		if nouns < 1 and verbs < 1:
			return True
	return False


def filter(sent):
	# Filter sentence if it doesn't follow the following rules:
	sent = " ".join(sent)
	return len(sent) > 400 or len(sent) < 10 \
		or sent.count(".") > 15 or not sent.isascii() \
		or not is_sentence(sent) 


if __name__ == "__main__":
	# Load up spacy

	# Open pdf file
	pdf_file = open("MazidiBook.pdf", "rb")
	pdf_reader = PyPDF2.PdfFileReader(pdf_file)

	# content is on pages [13,263]
	start_page = 13
	end_page = 263
	pages = [p for p in range(start_page, end_page+1)]

	# Ignore the index pages
	page_blacklist = [15,55,99,131,173,231,261]
	text = ""

	# For each page, extract text and add to our text list
	for i in [p for p in pages if p not in page_blacklist]:
		page = pdf_reader.getPage(i)
		text += " " + page.extractText().encode('utf-8').decode('ascii', 'ignore')
	pdf_file.close()

	text = ' '.join(text.split())
	text = text.replace("*** Draft copy of NLP with Python by Karen Mazidi: Do not distribute ***", "")	
	sents = sent_tokenize(text) # Split text into sentences

	# Initialize KB dictionary
	kb = {}

	# Extract keywords from our text
	extractor = yake.KeywordExtractor(top=1500, stopwords=stop_words)
	kb["keywords"] = [kw.lower() for kw, v in extractor.extract_keywords(text.lower())]

	# Create sentence lookup table 
	num_filtered = 0
	num_added = 0
	kb["lookup"] = {}
	for keyword in kb["keywords"]:
		kb["lookup"][keyword] = []
		for sent in sents:
			if keyword in sent.lower():
				if not filter(sent):
					kb["lookup"][keyword].append(sent)
					num_added += 1
				else:
					num_filtered += 1


	print(f"Added {num_added} sentences.")
	print(f"Filtered {num_filtered} sentences.")
	# Dump pickle file
	pickle_file = open("mazidi_book_kb.p", "wb")
	pickle.dump(kb, pickle_file)
	pickle_file.close()
