CHECKEDFILE = "all_checked_words" # File name for subfolder containing already collected results

# Imports
import os
from pathlib import Path

# Gets cwd
cwd = Path(os.getcwd())

# Overwrites the checkedwords.txt file to prevent repeats
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'r') as file:
    checked_words = list(set([line.strip() for line in file]))
checked_words = sorted(list(set(checked_words)))
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedwords.txt"]), 'w') as file:
    file.write('\n'.join(checked_words))

# Over-writes the checkedleaderboard.txt file to prevent repeats
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'r') as file:
    checked_words = list(set([line.strip() for line in file]))
checked_words = sorted(list(set(checked_words)))
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'w') as file:
    file.write('\n'.join(checked_words))

# Re-writes the checkedleaderboard.txt file in score order
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\checkedleaderboard.txt"]), 'r') as file:
    checked_words = list(set([line.strip() for line in file]))
checked_words = sorted(checked_words, key=lambda x: float(x[6:]), reverse=True)
with open(str(cwd) + "".join(["\\", CHECKEDFILE, "\\leaderboard_ordered.txt"]), 'w') as file:
    file.write('\n'.join(checked_words))

print("done!")