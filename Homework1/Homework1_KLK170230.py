"""
    Name:   Kathryn Kingsley
    UTID:   KLK170230
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for Homework 1. It contains a main() driver
            function along with 5 operational functions.

"""
import sys  # to use system parameters
import pathlib  # to read the input file
import re  # for regex
import pickle  # for pickling

'''
Person is a class to keep all of my objects organized.
In the homework1 system, all people must have first, last, 
and middle names as well as a phone number and ID. 

'''


class Person:
    # class constructor
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        return ('\nEmployee id: {}\n\t{} {} {}\n\t{}'.format(self.id, self.last, self.mi,
                                                             self.first, self.phone))


'''
phone_format() takes on the task of checking and altering
any phone numbers in the input file. It takes in a
phone number and uses regex to pattern check. It returns 
a formatted number

'''


def phone_format(phone):
    # check if phone number is in the correct format
    while not re.match(r'^\d{3}[.\s]?\d{3}[-.\s]?\d{4}', phone):
        phone = input(
            "\nPhone {} is invalid.\nEnter phone number in form ###-###-####. \nPlease enter a valid phone "
            "number or hit \'x\' to exit the program: ".format(phone))
        if phone == 'x':
            exit()
        # code if phone number is in the right format
        if re.match(r'^\d{3}-\d{3}-\d{4}', phone):
            return str(phone)
    # strip phone of all whitespaces and extra characters
    str_phone = re.sub(r'\D', '', str(phone))
    str_phone = str_phone[:3] + '-' + str_phone[3:6] + '-' + str_phone[6:]
    return str_phone


'''
id_format() takes on the task of checking and altering
any IDs in the input file. It takes in an
ID and uses regex to pattern check. It returns 
a formatted ID

'''


def id_format(user_id):
    # check if user_id is in the correct format
    while not re.match(r'[a-zA-Z]{2}\d{4}', user_id):
        user_id = input(
            "\nID invalid: {} \nID should have 2 letters followed by 4 numbers. \nPlease enter a valid ID or hit "
            "\'x\' to exit the program:".format(user_id))
        if user_id == 'x':
            exit()
    str_id = str(user_id[0]).upper() + str(user_id[1]).upper() + str(user_id[2:])
    return str_id


'''
capital_case_format() takes on the task of checking and altering
any name- first, middle, and last-  in the input file. 
It takes in a name and coverts just the first letter 
to capital. It returns a properly formatted name

'''


def capital_case_format(name):
    # if there is no name, make it X
    if not name:
        str_name = 'X'
    else:
        # convert to string just in case
        # put in title format (capital case)
        str_name = str(name).title()
    return str_name


'''
line_process() does most of the processing for the program.
It takes in all lines of the file and tokenizes them. Then
these tokens are sent to respective formatting functions.
It takes the lines as an argument and returns a dictionary
of people.

'''


def line_process(lines):
    if not lines:
        print("There are no lines. Exiting program...")
        exit(3)
    else:
        people_dictionary = {}
        for line in lines:
            # convert all tokens to string
            tokens = line.split(",")
            # make sure there are enough tokens
            if len(tokens) >= 5:
                # send tokens to formatting methods
                last = capital_case_format(tokens[0])
                first = capital_case_format(tokens[1])
                middle = capital_case_format(tokens[2])
                user_id = id_format(tokens[3])
                phone = phone_format(tokens[4])
                # create Person
                person = Person(last, first, middle, user_id, phone)
                # check if person already exists
                if person.id in people_dictionary:
                    print("Error: duplicate ID entry. Exiting...")
                    exit(3)
                else:
                    people_dictionary[person.id] = person
    return people_dictionary


'''
File_process() takes a full filepath argument.
It then splits the text into lines and removes the 
header. A list of lines is returned. 
'''


def file_process(filepath):
    # empty list to store lines
    text_in = []
    if not filepath:
        print("Issue with opening file. Exiting program...")
        exit(2)
    # open file located at file path and read line by line
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()
    # close what you opened
    f.close()
    # get rid of header line
    for line in lines[1:]:
        text_in.append(line)
    return text_in


'''
main() is the driver function for the program.
It takes a filepath argument and forms the filepath.
Then the operational methods are called in order.  
'''


def main(filepath):
    full_path = pathlib.Path.cwd().joinpath(filepath)
    # stage 1
    text = file_process(full_path)
    # stage 2
    person_dict = line_process(text)
    # stage 3- all things pickle
    pickle.dump(person_dict, open('ppl_pickle.p', 'wb'))
    pickle_people = pickle.load(open('ppl_pickle.p', 'rb'))
    # print the pickle
    print("\nEmployee list:")
    for person_id in pickle_people:
        print(pickle_people[person_id].display())


'''
Function so that this program can be run from the command
line. It doesn't do much except check that a file argument
was entered and pass control to main().

'''

if __name__ == '__main__':
    fp = ''
    if len(sys.argv) == 1:
        print("Please enter a filename. Exiting program.")
        exit(1)
    else:
        fp = sys.argv[1]
    main(fp)
