# OptimalWordleWord
Code and source data to try and find the optimal first Wordle Word by calculating expected information gain. Base e is used for entropy calculations. Does not take into consideration what the second, third, or fourth word will be. Currently in the process of expanding functionality.
Code is sloppy and unoptimised, insufficient for bots or automated programs. My first time using gitHub so it's a HelloWorld moment.

Constants:
The constant ITERLEN contains a number that contains the amount of words the code will evaluate at a time. The constant CHECKLEADERBOARD should be set to TRUE if you want to see the results, and LDB_LEN can be changed for how many results you want to see. The constant IGNORE is a list of the sourceword files you specifically do not want the program to access for whatever reasons. The constant DEBUG_METHOD should be set to TRUE whenever you want to watch the program go fast and run properly, and you'll need to change ITERLEN to a nice small value (1-200) if you're doing that. START_FROM_SCRATCH should be set to TRUE if you don't want the previous execution's information impacting this one's. PRINTOUT should be set to true if you'd like an extra file containing the entire leaderboard.

Either DEBUG_METHOD, ABSOLUTE_METHOD, or SHUFFLER_METHOD should be set to "True". Only one should be true at a time. DEBUG_METHOD runs the code on a small, randomised slice of words to make sure that it runs okay. ABSOLUTE_METHOD runs the entire process: comparing all word list words (that aren't in IGNORE) against each other. Takes a very long while and runs on O(n^2) time, where n is the total number of words. It's intended to run intermittently, and save the results after each go. For the full list, it'll take about two weeks to run. Alternatively, the SHUFFLER_METHOD takes random subsets of the list of size ITERLEN and estimates the expected information gain by comparing within the set, and then does that across the entire word list. Much faster. More accurate with higher n, but takes more time.  

"centralcode.py" is now parallelised! Feel free to run a couple of terminals to shorten the process. Run "cleanlists.py" after running the central code. This creates additional storage files with cleaner representations of the script's findings.


Files:
Contains the programs "centralcode.py" and "cleanlists.py" of my own design. Runs in python, in the same directory as your "sourcewords" folder.

The .txt files present in the "sourcewords" folder are not my own and have not been collected or collated by me. Any user of this code may add their own .txt files containing lists of words, although note that the code is designed specifically for six-word systems.

The files currently present are attributed as follows:
"5-letter-words.txt" published by daemondevin on gitHub 
"5-letters.txt" published by Blkzer0 on gitHub
"valid-wordle-words" published by dracos on gitHub
"wordle-answers-alphabetical" published by cfreshman on gitHub 
"reubens_wordle_words" curated by me
Code directly imitates the game "Wordle" designed by Josh Wardle. Yes, that's his real name.

The code will also create a folder within the directory containing the results (2-3 .txt files): both a list of all words already checked, and the results of their respective expected information gain statistics. 

Made for Windows. Linux/MacOS attempts will likely encounter some path errors.


If you're wondering what my results were, it'll take a while but right now the winners are "SLATE", "SABES", a few others. More testing to follow. The worst is "Xylyl".
