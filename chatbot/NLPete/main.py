import config as cfg
import pickle
import random
import spacy
import time

from nltk.corpus import stopwords
from screen import Screen

stop_words = stopwords.words("english")
nlp = spacy.load('en_core_web_md')
kb = pickle.load(open("mazidi_book_kb.p", "rb"))
choose = lambda arr: random.choice(arr)


# Returns true if any item in arr is present in text
def find_occurrence(arr, text):
    for word in arr:
        if word in text:
            return True
    return False

class ChatBot:

    def __init__(self, name):        
        self.name = name  # chat bot's name      
        self.user_name = "" # user's name
        self.name_response_idx = 0 # keeps track of response for name
        self.confused_response_idx = 0 # keeps track of response for confusion
        self.screen = Screen() # Initialize screen object
        # Lists for user likes and dislikes
        self.likes_list = []
        self.dislikes_list = []

    # This function contains all of the major logic for the chatbot. 
    # It is called every time the user submits input.
    def respond(self, user_input):
        # Prep input
        user_input = user_input.lower()
        doc = nlp(user_input)
        
        response = ""
        if new_name := self.find_name(doc): # If user told us their name, respond and update name
            response = cfg.NAME_RESPONSES[self.name_response_idx].format(
                name=self.user_name,
                new_name=new_name
                )
            self.update_name(new_name)
        elif word := self.find_like(doc):
            # User told us they like a word. Add the like and respond accordingly
            # If the user changed their mind, indicate that you realized it
            changed = self.add_like(word)
            if changed:
                response = choose(cfg.LIKE_CHANGE).format(word=word)
            else:
                response = choose(cfg.LIKE_RESPONSES).format(word=word)
        elif word := self.find_dislike(doc):
            # User told us they dislike a word. Add the dislike and respond accordingly
            # If the user changed their mind, indicate that you realized it
            changed = self.add_dislike(word)
            if changed:
                response = choose(cfg.DISLIKE_CHANGE).format(word=word)
            else:
                response = choose(cfg.DISLIKE_RESPONSES).format(word=word)
        else:

            # If the user likes/dislikes a topic, prepend a little quip about it
            if word := self.likes(user_input):
                response = choose(cfg.LIKE_PREPENDS).format(word=word) + " "
            elif find_occurrence(self.dislikes_list, user_input):
                response = choose(cfg.DISLIKE_PREPENDS).format(word=word) + " "

            # See if the input text contains keywords
            if find_occurrence(kb["keywords"], user_input):
                responses = []
                # If it does, compile a list of all of the keywords. 
                # Then, add all of the associated responses to our response pool
                for token in doc:
                    if token.text in kb["keywords"]:
                        responses.extend(kb["lookup"][token.text])
                if len(responses) > 0:
                    # If we got a response, then choose a random one and append it to our response.
                    response += choose(responses)

        # If we weren't able to produce a response, simply 
        if response == "":
            response = cfg.CONFUSED[self.confused_response_idx]
            # Increment response so we don't give the same one multiple times
            self.confused_response_idx = (self.confused_response_idx + 1) % len(cfg.CONFUSED)
        self.chat(response)

    def likes(self, user_input):
        for word in self.likes_list:
            if word in user_input:
                return word

    def dislikes(self, user_input):
        for word in self.dislikes_list:
            if word in user_input:
                return word

    def find_like(self, doc):
        # Look for an occurrence of a like verb. If we find one, return the word.
        word = None
        if find_occurrence(cfg.LIKE_VERBS, doc.text) and not "don't like" in doc.text and not "dont like" in doc.text:
            for token in doc:
                # Find the token that's the object of the sentence and return it
                if ("dobj" in token.dep_):
                    word = token.text
                    break
        return word

    def find_dislike(self, doc):
        # Look for an occurrence of a dislike verb. If we find one, return the word.
        word = None
        if find_occurrence(cfg.DISLIKE_VERBS, doc.text):
            for token in doc:
                # Find the token that's the object of the sentence and return it
                if ("dobj" in token.dep_):
                    word = token.text
                    break
        return word

    def find_name(self, doc):
        # Look for an occurrence of a name verb. If we find one, return the word.
        name = None
        if find_occurrence(cfg.NAME_VERBS, doc.text):
            for token in doc:
                print
                if token.pos_ == "PROPN":
                    name = token.text
        return name

    # Add word to like list and check if the user changed their mind
    def add_like(self, word):
        self.likes_list.append(word)
        if word in self.dislikes_list:
            self.dislikes_list.remove(word)
            return True
        else:
            return False

    # Add word to dislike list and check if the user changed their mind
    def add_dislike(self, word):
        self.dislikes_list.append(word)
        if word in self.likes_list:
            self.likes_list.remove(word)
            return True
        else:
            return False
       

    # Update the user's name and progress the name shtick
    def update_name(self, new_name):
        self.screen.user_name = new_name
        # Progress name shtick
        if self.name_response_idx < len(cfg.NAME_RESPONSES)-1:
            self.name_response_idx += 1

    # Function to add bot's chat to the screen
    def chat(self, msg):
        # Make it look like he's thinking
        time.sleep(random.uniform(0.5, 1.5))
        self.screen.add_chat(self.name, msg)

    # Main loop for the chatbot. This runs until the user says goodbye or tries to exit.
    def run(self):
        self.screen.update()
        self.chat(cfg.INTRO) # Make bot chat the intro
        self.screen.update()
        while True:
            # Update the screen
            self.screen.update()
            res = self.screen.step()
            if res in cfg.EXIT_WORDS: # If user wants to exit, let them go peacefully
                self.chat(choose(cfg.GOODBYES))
                self.screen.update(True)
                self.dump()
                break
            elif res is not None: # The user chatted something, so respond to it.
                self.screen.update(True)
                self.respond(res)

    # Dump user state to a text file.
    def dump(self):
        f = open("user_state.txt", "w")
        f.write(f"User Name: {self.screen.user_name}\n")
        f.write("User likes: " + ", ".join(self.likes_list) + "\n")
        f.write("User dislikes: " + ", ".join(self.dislikes_list) + "\n")
        f.write("Chat log: \n")
        for line in self.screen.chat:
            f.write(line + "\n")


if __name__ == "__main__":
    chatbot = ChatBot("NLPete")
    chatbot.run()