ITERLEN = 3 # The amount of words tested at a time
LDB_LEN = 100 # The amount of results you'd like to see. Must be less than double ITERLEN if using debug method
IGNORE = ["5-letter-words.txt", "5-letters.txt"] # Files you don't want to pull words from
ABSOLUTE_METHOD = True # Set to true if you want the absolute method. See README for details
SHUFFLER_METHOD = False # Set to true if you want the shuffler method. See README for details
DEBUG_METHOD = False # Do you want to run on only a slice?
DEBUG_SIZE = ITERLEN # How big do you want that slice to be? Copies ITERLEN value, so go change that
START_FROM_SCRATCH = False # Do you want to reset your leaderboard data every time you run?
PRINTOUT = False # Set to true if you want a printed-out file containing the results
CHECKLEADERBOARD = False

GUESS_MATRIX = [[("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")], # Letters are tagged with "y", "g", "n" for "yellow",
                [("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")], # "green", or "none (grey)". Actual letters are capital.
                [("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")], # Examples: "A,g", "P,n", "J,y", "K,y", etc.
                [("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")], # An empty cell is denoted by *,*
                [("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")],
                [("*","*"), ("*","*"), ("*","*"), ("*","*"), ("*","*")]]

CHECKEDFILE = "all_checked_words" # File name for subfolder containing already collected results

# Imports
import os
import math
from pathlib import Path
import random
cwd = Path(os.getcwd())
wordswd = Path(str(cwd) + "//sourcewords")

# Resets the savedata files
if START_FROM_SCRATCH:
    for file in (cwd / CHECKEDFILE).iterdir():
        with open(str(file), "w") as file:
            pass

# Sets up method variable, checks for basic constant errors
if SHUFFLER_METHOD:
    method = "shuffler"
if DEBUG_METHOD:
    method = "debug"
if ABSOLUTE_METHOD:
    method = "absolute"
if int(SHUFFLER_METHOD) + int(ABSOLUTE_METHOD) + int(DEBUG_METHOD) != 1:
    raise ValueError("Only one of the method constants may be set to True")
if DEBUG_METHOD and (ITERLEN < LDB_LEN):
    raise ValueError("ITERLEN cannot be set to less than LDB_LEN. Either lower LDB_LEN (recommended) or raise ITERLEN")


# Takes the file name of the list and returns the words, formatted as a list
def list_extract(file_name):
    master_word_list = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            master_word_list.append(line.strip())
    return master_word_list

# Returns an element options list based on a given guess matrix
def get_element_options(guess_matrix, word_list):
    # Gets the options BEFORE you consider the guess matrix data
    # Finds the possibilities for each letter slot
    i = 0
    options = []
    while i < len(word_list[0]):
        slot_options = []
        for word in word_list:
            slot_options.append((word[i]).upper())
        slot_options = sorted(set(slot_options))
        options.append(slot_options)
        i = i + 1

    # Cleans options based on guess matrix data
    # Logic Used:
    # 1 If a cell is green, then there is only one possible option for that cell
    # 2 If a cell is green, and another cell with the same letter is grey, then that letter must be removed from all options except the green cell
    # 3 If a cell is green, and another cell with the same letter is yellow, then that comes under the provision where yellow letters need to be narrowed down
    # 4 If a cell is grey, then that cell may not contain that letter
    # 5 If a cell is grey, and no other instances of that letter appear in the word, remove the grey from all slot options
    # 6 If a cell is yellow, then that cell may not contain that letter
    # 7 If a cell is yellow, and there is only one possible place that yellow could go, that cell must be assigned green with that letter
    
    # Handles Single-Colour implications (1,4,6)
    i = 0
    for slot in options:
        for guess in guess_matrix:
            letter = guess[i][0]
            colour = guess[i][1]
            if colour == "g":
                options[i] = [letter]
            elif colour == "y" or colour == "n":
                for op in slot:
                    if op == letter:
                        (options[i]).remove(op)
        i = i + 1

    # Handles single-instance greys (5)
    for guess in guess_matrix:
        for element in guess:
            letter = element[0]
            colour = element[1]
            if colour == "n":
                amount = 0
                for elem in guess:
                    if elem[0] == letter:
                        amount = amount + 1
                if amount == 1:
                    i = 0
                    for slot in options:
                        for op in slot:
                            if op == letter:
                                (options[i]).remove(op)
                        i = i + 1

    # Handles (2): Mixed greens and greys
    for guess in guess_matrix:
        for element in guess:
            letter = element[0]
            amount = 0
            for elem in guess:
                if elem[0] == letter:
                    amount = amount + 1
            if amount > 1:
                amt_green = 0
                amt_grey = 0 
                greens = []
                i = 0
                for elem in guess:
                    if (elem[0] == letter) and (elem[1] == "g"):
                        amt_green = amt_green + 1
                        greens.append(i)
                    elif (elem[0] == letter) and (elem[1] == "n"):
                        amt_grey = amt_grey + 1
                    i = i + 1
                if (amt_green >= 1) and (amt_grey >= 1):
                    i = 0
                    for elem in guess:
                        if i not in greens:
                            if letter in options[i]:
                                (options[i]).remove(letter)
                        i = i + 1
    # Handles yellows in cases 3 and 7. Loops until equilibrium
    update = True
    while (update == True):
        update = False
        none_are_yellow = True
        for guess in guess_matrix:
            for elem in guess:
                if elem[1] == "y":
                    none_are_yellow = False
        if none_are_yellow:
            break
        for guess in guess_matrix:
            for element in guess:
                letter = element[0]
                colour = element[1]
                if colour == "y":
                    # Handles case 7
                    amt_yellows = 0
                    for elem in guess:
                        if (elem[0] == letter) and (elem[1] == colour):
                            amt_yellows = amt_yellows + 1
                    choices = 0
                    i = 0
                    spots = []
                    for slot in options:
                        if letter in slot:
                            choices = choices + 1
                            spots.append(i)
                        i = i + 1
                    if choices == amt_yellows:
                        for spt in spots:
                            if options[spt] != [letter]:
                                options[spt] = [letter]
                                update = True

                    # Case 3
                    # If an element is yellow in conjuction with a green, assign it into any green slot that is not that slot,
                    # If no such option slot exist, pigeonhole it into any remaining slot
                    i = 0
                    for elem in guess:
                        amt_greens = 0
                        green_slots = []
                        if (elem[0] == letter) and (elem[1] == "g"):
                            green_slots.append(i)
                            amt_greens = amt_greens + 1
                        amt_yellows = 0
                        for elem in guess:
                            if (elem[0] == letter) and (elem[1] == colour):
                                amt_yellows = amt_yellows + 1
                        i = i + 1
                    choices = 0
                    i = 0
                    spots = []
                    for slot in options:
                        if letter in slot:
                            choices = choices + 1
                            spots.append(i)
                        i = i + 1

                    if amt_yellows == choices - amt_greens:
                        for spt in spots:
                            if options[spt] != [letter]: 
                                options[spt] = [letter]
                                update = True 

    # Recalculates the word list based on this new abbreviated options list
    removables = []
    rem_word_list = word_list.copy()
    for word in rem_word_list:
        i = 0
        for letter in word:
            if (letter.upper() not in options[i]) and (word not in removables):
                removables.append(word)
            i = i + 1
    for remov in removables:
        rem_word_list.remove(remov)

    # Generates a new options list with probabilities for this new word list
    n = len(rem_word_list)
    options = []
    for i in [0,1,2,3,4]:
        slot = []
        for word in rem_word_list:
            letter = word[i]
            isin = 0
            for op in slot:
                if op[0] == letter:
                    isin = 1
                    op[1] = op[1] + 1
            if not isin:
                slot.append([letter, 1])
        options.append(slot.copy())
    for slot in options:
        for elem in slot:
            elem[1] = float(elem[1]) / float(n)

    return options

# Calculates the entropy of an options matrix. Assumes the cells are independent. They probably aren't
def entropy_of_options(options):
    total_entropy = float(0)
    for slot in options:
        slot_entropy = float(0)
        for opt in slot:
            slot_entropy = slot_entropy + opt[1] * math.log(opt[1], math.e)
        slot_entropy = slot_entropy * -1
        total_entropy = total_entropy + slot_entropy
    return total_entropy

# Takes a true word and guess word and returns a colour string of the form "ngyyn"
def wordle(true_word, guess_word):
    col_answer = ["n","n","n","n","n"]
    i = 0
    for letter in guess_word:
        if letter == true_word[i]:
            col_answer[i] = "g"
        if (letter in true_word) and (letter != true_word[i]):
            amount = 0
            for let in true_word:
                if let == letter:
                    amount = amount + 1
            j = 0
            for let in guess_word:
                if j < i:
                    if let == letter:
                        amount = amount - 1
                if j == i:
                    if amount > 0:
                        col_answer[i] = "y"
                j = j + 1
        i = i + 1
    return col_answer


# My preferred word decision algorithm, as described above
def golden_algorithm(guess_matrix, word_list, master_word_list):
    print("=======================")
    letter_options = get_element_options(guess_matrix, master_word_list)
    base_entropy = entropy_of_options(letter_options)

    # Loops through each possible word to find the best opener
    leaderboard = []
    num_checks = len(word_list)
    check = 1
    for test_word in word_list:
        # Acquires the probability of each colour convolution
        # print("Checking", check, "//", num_checks, "---", test_word)
        convolutions = []
        for word in master_word_list:
            result = wordle(word, test_word)
            found = False
            for conv in convolutions:
                if result == conv[0]:
                    conv[1] = conv[1] + 1
                    found = True
            if not found:
                convolutions.append([result, 1])
        n = len(master_word_list)
        for conv in convolutions:
            conv[1] = float(conv[1]) / float(n)
        # Finds the expected information gain of each convolution
        new_line = 0
        for guess in guess_matrix:
            if guess[0][0] == "*":
                break
            new_line = new_line + 1 
        ex_infogain = 0
        for conv in convolutions:
            test_guess_matrix = guess_matrix.copy()
            test_guess = []
            i = 0
            for col in conv[0]:
                test_guess.append(((test_word[i]).upper(), col))
                i = i + 1
            test_guess_matrix[new_line] = test_guess
            options = get_element_options(test_guess_matrix, master_word_list)
            test_entropy = entropy_of_options(options)
            infogain = base_entropy - test_entropy
            ex_infogain = ex_infogain + infogain * conv[1]
        # print(test_word, "Tested: Expected infogain:", ex_infogain, "nats")

        # Checks the leaderboard and updates it based on what's best
        leaderboard.append([test_word, ex_infogain])
        check = check + 1
    past_words = list_extract(cwd / CHECKEDFILE / "checkedwords.txt")
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), "a") as file:
        for word in leaderboard:
            if word[0] not in past_words:
                file.write(word[0] + "\n")
        file.close()
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), "a") as file:
        for word in leaderboard:
            if word[0] not in past_words:
                file.write(word[0] + "~" + str(word[1]) + "\n")
        file.close()
                   
# ACTIVE CODE BELOW

# Acquires all possible words it could be, searching word lists that aren't in IGNORE
print("Acquiring Words")
master_word_list = []
for wordlist in wordswd.iterdir():
    ignore_p = False
    for ig in IGNORE:
        if ig in str(wordlist):
            ignore_p = True  
    if not ignore_p:
        list_word_list = list_extract(wordlist)
        print("Extracting from", wordlist, "||", len(list_word_list), "words testable")
        for elem in list_word_list:
            if elem not in master_word_list:
                master_word_list.append(elem)

# Just if you want to run it super quickly to test for kinks
if DEBUG_METHOD:
    print("Running Debug Method:")
    random.shuffle(master_word_list) # TEST REMOVE LATER
    master_word_list = master_word_list[0:DEBUG_SIZE] # TEST REMOVE LATER
unchecked_words_list = master_word_list.copy()

# Removes all the previously checked words from the list
checkedwords = 0
if cwd / CHECKEDFILE in cwd.iterdir():
    if (CHECKEDFILE + "\\checkedwords.txt") not in str(cwd / CHECKEDFILE):
        with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), "a") as file:
            file.close()
        with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), "a") as file:
            file.close()
    list_word_list = list_extract(CHECKEDFILE + "\\checkedwords.txt")
    checkedwords = len(list_word_list)
    print("Already checked words: ", checkedwords)
    for word in list_word_list:
        if word in unchecked_words_list:
            unchecked_words_list.remove(word)
        
# Create a file for all the checked words
if cwd / CHECKEDFILE not in cwd.iterdir():
    os.makedirs(str(cwd) + "".join(["\\", CHECKEDFILE]), exist_ok=True)

print("=========================")
print("Total Wordlist Found:", len(master_word_list), "words testable")
print("Unchecked words", len(unchecked_words_list), "+ checked words", checkedwords, "=", checkedwords + len(unchecked_words_list))
print("Thus far ", (checkedwords / len(master_word_list)) * 100, "% checked")
print("=========================")

# If there's still work to be done
if len(unchecked_words_list) != 0:
    # Runs the Absolute Method (See README for details)
    if ABSOLUTE_METHOD:
        print("Running Absolute Method:")
        print(ITERLEN, "Words to run")
        # Takes ITERDIR number of words, tests them, adds them to the leaderboard
        if len(unchecked_words_list) > ITERLEN:
            golden_algorithm(GUESS_MATRIX, unchecked_words_list[0:ITERLEN], master_word_list)
        else: 
            golden_algorithm(GUESS_MATRIX, unchecked_words_list, master_word_list)

    # Runs the Shuffler Method (See README for details)
    if SHUFFLER_METHOD:
        print("Running shuffler method:")
        numwhole = len(unchecked_words_list) // ITERLEN
        random.shuffle(unchecked_words_list)
        if len(unchecked_words_list) >= ITERLEN:
            diff = len(unchecked_words_list) - numwhole*ITERLEN
        else:
            diff = len(unchecked_words_list)
        print(str(numwhole), "slices necessary of size ", ITERLEN, "and one of size", diff)
        i = 0
        for i in range(numwhole):
            print("Running slice", str(i + 1), "//" , str(numwhole + 1))
            golden_algorithm(GUESS_MATRIX, unchecked_words_list[i * ITERLEN:(i + 1)*ITERLEN], unchecked_words_list[i * ITERLEN:(i + 1)*ITERLEN])
            i = i + 1
        print("running final slice")
        difflist = random.sample(unchecked_words_list[:numwhole * ITERLEN], diff)
        lastslice = difflist + unchecked_words_list[numwhole*ITERLEN:]
        golden_algorithm(GUESS_MATRIX, lastslice, lastslice)

print("Methodology Completed")

# Extracts the leaderboard and produces results
if CHECKLEADERBOARD:
    leaderboard = list_extract(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]))
    print(len(leaderboard), "words checked")
    ldb = []
    for line in leaderboard:
        line = "".join(line.split())
        data = line.split("~")
        ldb.append((data[0], data[1]))
    ldb = sorted(ldb, key=lambda x: x[1])
    print("WORST WORDS:\n=============")
    for i in range(LDB_LEN):
        print(">", ldb[i][0], "---", "EX INFOGAIN", ldb[i][1], "nats")
    print("BEST WORDS:\n=============")
    for i in range(checkedwords - LDB_LEN, checkedwords):
        print(">", ldb[i][0], "---", "EX INFOGAIN", ldb[i][1], "nats")

    # Writes total leaderboard output into a file 
    if PRINTOUT:
        with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\finalresults.txt"]), "w") as file:
            file.write("Produced using the" + method + "method with ITERLEN" + str(ITERLEN) + "\n")
            for word in sorted(ldb, key=lambda x: x[1], reverse=True):
                file.write(word[0] + "--- EIG ~ " + word[1] + "\n")
            file.close()