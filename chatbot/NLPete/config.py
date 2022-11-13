##########################################################
#------------------Chatbot definitions-------------------#
##########################################################

INTRO = "Hi! I'm NLPete, your comprehensive guide on natural language processing! What's your name?"

EXIT_WORDS = ["break", "quit", "goodbye", "bye", "exit", "let me out", ":wq", ":q"]

GOODBYES = ["Bye, have a nice day!", "Thanks for talking with me!", "Leaving so soon? Okay :("]

LIKE_VERBS = ["like", "enjoy", "love", "i'm into"]

DISLIKE_VERBS = ["hate", "sucks", "awful", "dont like", "don't like"]

NAME_VERBS = ["name", "call", "llamo", "named", "i'm"]

CONFUSED = ["I'm confused... Can we change the subject?",
            "That went straight over my head. Can we move on?",
            "I'm sorry, I honestly have no clue what you just said.",
            "Dude I lost you at the first word. Could you try a different question?",
            "I think I forgot some tokens, I have no idea what you mean by that.",
            "Huh..?",
            "What..?",
            "Thats crazy.",
            "Was that english?",
            "Sorry, I fell asleep lol. Could you say that again?"]

NAME_RESPONSES = ["Nice to meet you, {new_name}! How can I help you today?",
                  "Shoot, sorry {new_name}, I thought your name was {name}...",
                  "I'm losing patience with you, {new_name}",
                  "I give up. I'll call you Pete from now on.",
                  "..."]

LIKE_RESPONSES = ["No way, I like {word} too!",
                  "Me too, {word} is sweet!",
                  "Cool! Let me tell you more about {word}"]
LIKE_PREPENDS = ["I know you're excited about {word}, so check this out!",
                 "Your favorite, {word}!",
                 "I can't get enough of {word}!",
                 "Wow, you really like {word}, huh?",
                 "More {word}? Okay!"]

DISLIKE_RESPONSES = ["Oh, really? I thought {word} was kind of cool...",
                     "That's fine, I guess. It's not like {word} is my favorite or anything...",
                     "That sucks, {word} is very interesting!",
                     "Yeah, a lot of people don't like {word} for some reason."]
DISLIKE_PREPENDS = ["I know you don't like {word}, so let's skip this one.",
                    "Really, {word}? I thought you didn't like {word}.",
                    "I didn't think that you liked {word}."]

LIKE_CHANGE = ["I thought you didn't like {word}! I'll keep that in mind",
               "I didn't know that you were into {word}! I'll remember that.",
               "Oh, really? I'll talk about {word} more then."]
DISLIKE_CHANGE = ["I thought you liked {word}. Oh well, your loss.",
                  "Oh, really? Okay, I'll keep that in mind, I thought you were a fan of {word}",

]

##########################################################
#------------------Function definitions------------------#
##########################################################
def index(arr):
    res = []
    i = 0
    for x in arr:
        res.append((i,x))
        i += 1
    return res

def raw_str(s):
    return "\n".join(s.splitlines()[1:])

##########################################################
#-------------------Screen definitions-------------------#
##########################################################

HEADER = raw_str(r'''


    o-----------------------------------------------------------------o
    |                                                                 |
    |            _______ _____   ______         __                    |
    |           |    |  |     |_|   __ \.-----.|  |_.-----.           |
    |           |       |       |    __/|  -__||   _|  -__|           |
    |           |__|____|_______|___|   |_____||____|_____|           |
    |                by Katie Kingsley and Jonathan Yu                |        
    |                                                                 |
    o-----------------------------------------------------------------o''')
EULA=\
" Please note that this conversation may be monitored for quality assurance."
TOP = raw_str(r'''
    o-----------------------------------------------------------------o
    |                                                                 |''')
LINE = raw_str(r'''
    |                                                                 |''')
PROMPT = raw_str(r'''
    +-----------------------------------------------------------------+
    |  >                                                              |
    |                                                                 |''')
PROMPT_PAUSE = raw_str(r'''
    +-----------------------------------------------------------------+
    |                                                                 |
    |                                                                 |''')
BOTTOM = raw_str(r'''
    o-----------------------------------------------------------------o''')

POINTER_CHAR = "_"
INPUT_START = PROMPT.find(">") + 2

SCREEN_WIDTH = len(TOP.splitlines()[0])
SCREEN_HEIGHT = 30  

ARROW_KEYS = {b"H": "U", b"P": "D", b"K": "L", b"M": "R"}