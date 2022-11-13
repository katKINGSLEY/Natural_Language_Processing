import config as cfg
import msvcrt
import os


# This class manages all the text input and display in the command line terminal
class Screen:  

    # Initialize all relevant variables
    def __init__(self):
        self.pointer = 0
        self.current = []
        self.chat = []
        self.last = ""
        self.user_name = "Me"

    # This function handles user input
    def step(self):  
        # Get the latest key input byte
        key = msvcrt.getch()

        if key == b'\x03':
            # User pressed Ctrl+C, so exit the program
            return "break"
        elif self.last == b'\xe0':
            # Arrow keys are inputted as two bytes: a b'\xe0' followed by a K or M.
            #   We keep track of the last input to handle this edge case.
            # Arrow keys, move pointer
            if key == b"K":
                self.move_pointer(-1)
            elif key == b"M":
                self.move_pointer(1)
        elif key == b'\x08':
            # Backspace
            if len(self.current) > 0:
                self.current.pop(self.pointer-1) # Erase latest character
                self.pointer -= 1 # Move pointer back
        elif key == b'\r':
            # Enter (carriage return)
            if len(self.current) > 0:
                msg = "".join(self.current) # Turn current into a string
                self.add_chat(self.user_name, msg) # Add user's chat
                self.current.clear() # Clear current input
                self.pointer = 0 # Reset pointer to start
                return msg       
        elif key not in [b'\xe0', b'\t']:
            # This should be an alphanumeric input
            try:
                if len(self.current) < 59*2-2:
                    self.current.insert(self.pointer, key.decode())
                    self.pointer += 1
            except:
                pass

        # Used for handling arrow keys
        self.last = key
        # If the user didn't press enter, then nothing happened.
        return None

    def add_chat(self, user, msg):
        # Add chat to back of chat history
        self.chat.append(user)
        last = 0
        # Split the message into substrings of length 59, then print each.
        # Message definitely shouldn't be longer than 590 characters, as max input length is 
        #   59*2, and kb is filtered to sentences under 400 characters.
        for i in range(1,10):
            line = msg[last:last+59]
            if line == "":
                break
            last = last + 59
            self.chat.append(line)
        self.chat.append("")

    # This function wipes the terminal and prints the new "screen"" to the console.
    def update(self, thinking=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(cfg.HEADER)
        print()
        print(cfg.EULA)
        print(cfg.TOP)
        self.display_chat()
        self.display_input(thinking)
        print(cfg.BOTTOM)

    # Keep the pointer within bounds
    def move_pointer(self, move):
        if (move < 0 and self.pointer > 0)\
        or (move > 0 and self.pointer < 59*2 and self.pointer < len(self.current)):
            self.pointer += move


    # Display the current chat
    def display_chat(self):
        lines = []
        # Create list of modifiable output lines
        for i in range(cfg.SCREEN_HEIGHT-3):
            lines.append(list(cfg.LINE))

        msg_index = len(self.chat)-1
        # Starting from the bottom going up, change each line to the given text.
        for line in reversed(lines):
            # There's no more chats left
            if msg_index < 0:
                break
            start_pos = 9 # this is the start position of the line
            msg = self.chat[msg_index]
            if msg in [self.user_name, "Me", "NLPete"]:
                start_pos = 7 # If it's a user, move the name to the left.

            # Insert each character into the line
            for i, char in cfg.index(msg):
                line[start_pos + i] = char
            msg_index -= 1
        # Create the output
        print("\n".join(["".join(l) for l in lines]))


    # This function displays the user's current text input.
    def display_input(self, pause_input):
        assert len(self.current) < 59*2-1

        if not pause_input:
            str_len = len(self.current)
            new_str = list(cfg.PROMPT)
            offset = 0
            start_pos = cfg.INPUT_START
            # 
            for i, char in cfg.index(self.current):
                if i >= 59:
                    # Wrap text back to next line
                    start_pos = cfg.INPUT_START + 13
                if i == self.pointer:
                    # Insert pointer and make offset 1
                    offset = 1
                    new_str[start_pos + i] = cfg.POINTER_CHAR
                new_str[start_pos + i + offset] = char

            # Pointer wasn't inserted, so add it to the end
            if offset == 0:
                pos = start_pos + str_len
                if len(self.current) >= 58:
                    # If we're on the second line, make it wrap.
                    pos += 13
                new_str[start_pos + str_len] = cfg.POINTER_CHAR
            print("".join(new_str))
        else:
            print(cfg.PROMPT_PAUSE)


