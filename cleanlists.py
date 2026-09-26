CHECKEDFILES = ["all_checked_words_priors-NONE", "all_checked_words_priors-slate"] # File name for subfolder containing already collected results

# Imports
import os
from pathlib import Path

# Gets cwd
cwd = Path(os.getcwd())

# Iterates through each of the folders required
for CHECKEDFILE in CHECKEDFILES:

    # Checks 1:1 correlation between the two lists
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'r') as file:
        checked_words = list(set([line.strip() for line in file]))
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'r') as file:
        checked_words_leader = list(set([line.strip() for line in file]))

    # Checks the checked words against the leaderboard
    print("Checking for checked words' presence on leaderboard:")
    all_there = True
    remove = []
    for word in checked_words:
        found = False
        for ldb_entry in checked_words_leader:
            if word == ldb_entry[:5]:
                found = True
                break
        if not found:
            print("> removing", word)
            remove.append(word)
            all_there = False
    if all_there:
        print("= All checked words are represented in the leaderboard!")
    for rm in remove:
        checked_words.remove(rm)   

    # Checks the leaderboard words against the checked words
    print("Checking for leaderboard words' presence in the checked words:")
    all_there = True
    remove = []
    for word_entry in checked_words_leader:
        found = False
        word = word_entry[:5]
        for cw in checked_words:
            if word == cw:
                found = True
                break
        if not found:
            print("> removing", word_entry)
            remove.append(word_entry)
            all_there = False
    if all_there:
        print("= All leaderboard words are represented in the checked list!")
    for rm in remove:
        checked_words_leader.remove(rm)   

    # Writes them back in
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'w') as file:
        file.write('\n'.join(checked_words_leader))
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'w') as file:
        file.write('\n'.join(checked_words))


    # Re-writes the checkedleaderboard.txt file in score order
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'r') as file:
        checked_words = list(set([line.strip() for line in file]))
    if "" in checked_words:
        checked_words.remove("")
    checked_words = sorted(checked_words, key=lambda x: float(x[6:]), reverse=True)
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\leaderboard_ordered.txt"]), 'w') as file:
        file.write('\n'.join(checked_words))

    # Overwrites the checkedwords.txt file to prevent repeats
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'r') as file:
        checked_words = list(set([line.strip() for line in file]))
    if "" in checked_words:
        checked_words.remove("")
    checked_words = sorted(checked_words)
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'w') as file:
        file.write('\n'.join(checked_words))

    # Over-writes the checkedleaderboard.txt file to prevent repeats
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'r') as file:
        checked_words = list(set([line.strip() for line in file]))
    if "" in checked_words:
        checked_words.remove("")
    checked_words = sorted(checked_words)
    with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'w') as file:
        file.write('\n'.join(checked_words))

    print("Completed for", CHECKEDFILE)

