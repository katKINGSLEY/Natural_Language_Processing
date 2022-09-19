"""
    Name:   Kathryn Kingsley
    UTID:   KLK170230
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the Guessing Game assignment. It contains a main() driver
            function along with 2 classes and 7 operational functions.

"""
import pathlib  # for path
import sys  # to use system parameters
import nltk  # for part of speech tagging in preprocessing
from nltk.tokenize import word_tokenize  # to tokenize raw text
from nltk.corpus import stopwords  # to eliminate not functional words
from nltk.stem import WordNetLemmatizer  # for lemmatizing in preprocessing
from random import seed  # for random numbers
from random import randint  # for random numbers

'''
The Text class keeps all important information about the initially read text
in one place. It takes the file and reads it in as raw text and saves it. 
Cleaned tokens are not saved here even though they are used multiple times 
to abide by assignment specifications.

'''


class Text:
    # class constructor
    def __init__(self, file):
        self.lexical_diversity = 0
        # read in file as raw text
        if file:
            with open(file, 'r') as file:
                self.raw_text = file.read()
        else:
            print("Issue with opening file. Exiting program...")
            exit(2)
        # close the file
        file.close()


'''
The Game class is the main meat of the function. It stores all game 
related variables like the overall score and the word for a given round.
It also contains the instructions that print out before each game. This
class includes functions that carry out different game related tasks as 
well like creating a new round and handling when a guess is made. 

'''


class Game:

    # class constructor
    def __init__(self, words):
        self.overall_points = 5
        self.word_list = words
        self.word = ''
        self.guesses = []
        self.user_word = ''
        self.instructions = "\n******************************************Let's play a word guessing " \
                            "game!******************************************\n" \
                            "\n\t Guess letters in a mystery word. For each correct guess, a point" \
                            " will be awarded. For each incorrect guess, \n\t a point will be deducted." \
                            "\n\t\t - Points to start:   5" \
                            "\n\t\t - Quit at any time by entering '!' " \
                            "\n\t Play as many rounds as you want as long as your score is 0 or greater." \
                            "\n\nHere comes your first word: "

    # run whenever a word is successfully guessed.
    def new_round(self):
        # set seed to index is random
        seed(1234)
        # reset game variables for new round
        self.guesses = []
        self.user_word = ""
        self.word = ""
        # get random index between 1 and length of the word list
        index = randint(1, len(self.word_list) - 1)
        # assign the word and remove it
        self.word = self.word_list[index]
        self.word_list.remove(self.word_list[index])
        # create the blanks
        for letter in self.word:
            self.user_word += '_'
        # print(self.word)
        # add spaces for better readability
        print(' '.join(self.user_word))

    '''
    This function is run every time a letter is guessed. It checks that the entry is
    in the proper format and alerts the user if it is not. It is also the function
    that manages the user_word and the game points. 

    '''

    def make_guess(self, guess):
        temp_word = ''
        found_flag = False
        guess_points = 0
        # guess format check
        if guess == '!':
            return
        if len(guess) > 1:
            print("\n" + ' '.join(self.user_word))
            print("It appears that multiple items were entered. Please enter only 1 letter at a time.")
            return
        if len(guess) < 1 or guess == ' ':
            print("\n" + ' '.join(self.user_word))
            print("A letter was not entered. Please try again.")
            return
        if guess in self.guesses:
            print("\n" + ' '.join(self.user_word))
            print("Oops! You already guessed that letter. -1 point")
            self.overall_points -= 1
            print("Your score is now {}!".format(self.overall_points))
        else:
            for index, letter in enumerate(self.word):
                if guess == letter:
                    temp_word += letter
                    guess_points += 1
                    found_flag = True
                elif self.user_word[index].isalpha():
                    temp_word += self.user_word[index]
                else:
                    temp_word += '_'
            self.user_word = temp_word
            self.guesses.append(guess)
            print("\n" + ' '.join(self.user_word))
            if found_flag:
                print("Correct! The letter \'{}\' was in the word {} time/s!".format(guess, guess_points))
            else:
                print("Sorry. The letter \'{}\' did not appear in the word. You lost a point :(".format(guess))
                self.overall_points -= 1
            self.overall_points += guess_points
            print("Your score is now {}!".format(self.overall_points))
            return


'''
The play_game function is a while loop that is the game itself. It handles
the Game instance and coordinates function calls so that the game can be 
played according to the rules.

'''


def play_game(game):
    print(game.instructions)
    game.new_round()
    user_input = ''
    while (user_input != '!') and (game.overall_points >= 0):
        print("Previously guessed letters: ")
        print(game.guesses)
        user_input = input("Guess a letter: ")
        game.make_guess(user_input)
        if game.user_word == game.word:
            print(' '.join(game.user_word))
            print("\nCongratulations! You solved it! :) \n\nStarting another round!\n")
            game.new_round()
    if user_input == '!':
        print("\n*****Exiting the game. Thanks for playing!*****")
    if game.overall_points < 0:
        print(
            "\n Oh no! It looks like you have less than 0 points! \n The word was \'{}\'. \n Better luck next time!".format(
                game.word))
        exit(0)
    return


'''
get_lexical_diversity() takes a text argument that was created 
in main() and returns nothing. It takes all the raw tokens from the Text
class and cleans them up- removing all non-alpha tokens and stopwords, then 
converting them to lowercase. Then the lexical diversity rounded to 2
decimal places is output to the screen. Lexical diversity is calculated
as the number of unique, functional words divided by the total number
of functional words.

'''


def get_lexical_diversity(text):
    cleaned_tokens = [t.lower() for t in word_tokenize(text.raw_text) if t.isalpha()
                      and t not in stopwords.words('english')]
    text.lexical_diversity = len(set(cleaned_tokens)) / len(cleaned_tokens)
    print("\nLexical diversity: %.2f" % text.lexical_diversity)
    return


'''
Get_pos() takes tokens as an argument and returns a list of tuples that 
includes words and all parts of speech tags. First, the function assigns 
parts of speech to the input tokens. Then the first 20 parts of speech are 
printed as per assignment instructions.

'''


def get_pos(tokens):
    tags = nltk.pos_tag(tokens)
    print("\nFirst 20 POS tags: ")
    for tag in tags[:20]:
        print(tag)
    return tags


'''
get_noun_counts() is a quick helper function to double
check that the correct(ish) number of nouns are being
identified. It takes a list of tags and finds all where the 
POS begins with 'N' which equals a noun. The number changes
every time the program is run. 
'''


def get_noun_counts(tags):
    pos_dict = {}
    for token, pos in tags:
        if pos[0] == 'N':
            if pos not in pos_dict:
                pos_dict[pos] = 1
            else:
                pos_dict[pos] += 1
    for pos in sorted(pos_dict, key=pos_dict.get, reverse=True):
        print(pos, ':', pos_dict[pos])
    return


'''
Get_nouns() takes a list of tags as an argument and returns a 
list of all lemma from that text that are nouns. It does this
by checking that the first character in a given part of speech
beings with 'N'- indicating that it is a noun.
'''


def get_nouns(tags):
    nouns = []
    for token, pos in tags:
        if pos[0] == 'N':
            nouns.append(token)
    return nouns


'''
text_preprocess() takes a text argument and returns 2 lists: tokens and nouns. 
It prepares the raw text from a Text object. First, the text is tokenized, 
converted to all lower case, reduced to only alphabetical tokens, and 
limited to tokens that are at least 6 letters long. Then those tokens are
lemmatized.
'''


def text_preprocess(text):
    lemmatizer = WordNetLemmatizer()
    # step 1- clean and reduce text
    long_tokens = [t.lower() for t in word_tokenize(text.raw_text) if t.isalpha()
                   and t not in stopwords.words('english') and len(t) > 5]
    # step 2- get unique lemmas
    lem_long_tokens = [lemmatizer.lemmatize(t) for t in long_tokens]
    unique_long_tokens = set(lem_long_tokens)
    # step 3- POS tagging
    tags = get_pos(unique_long_tokens)
    # step 4- get list of nouns
    # get_noun_counts(tags)
    noun_tokens = get_nouns(tags)
    # step 5- print number of tokens
    print("\nTotal long tokens (step 1): " + str(len(long_tokens)))
    print("\nTotal noun tokens (step 4): " + str(len(noun_tokens)))
    return long_tokens, noun_tokens


'''
Create_game() takes a list of tokens representing the words from our
text and a list of nouns representing all the noun words from our text 
and creates the game from that. It does this by creating a dictionary
where a noun word is the key and the number of times that noun 
occurs within a text is the value. It then uses the 50 most common nouns 
from the text to create the guessing game. 
'''


def create_game(tokens, nouns):
    noun_dict = {}
    word_list = []
    for word in tokens:
        if word in nouns:
            if word not in noun_dict:
                noun_dict[word] = 1
            else:
                noun_dict[word] += 1
    for word in sorted(noun_dict, key=noun_dict.get, reverse=True)[:50]:
        # print(word, ':', noun_dict[word])
        word_list.append(word)
    game = Game(word_list)
    play_game(game)
    return


'''
main() is the driver function for the program.
It takes a filename argument and creates the Text 
class object.  
'''


def main(filename):
    # create File instance
    text = Text(pathlib.Path.cwd().joinpath(filename))
    get_lexical_diversity(text)
    tokens, nouns = text_preprocess(text)
    create_game(tokens, nouns)
    return


if __name__ == '__main__':
    fn = ''
    if len(sys.argv) == 1:
        print("Please enter a filename. Exiting program.")
        exit(1)
    else:
        fn = sys.argv[1]
    main(fn)
