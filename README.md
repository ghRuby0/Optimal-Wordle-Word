# OptimalWordleWord
Code and source data to try and find the optimal first Wordle Word by calculating expected information gain. Base e is used for entropy calculations. Does not take into consideration what the second, third, or fourth word will be.
Code is sloppy and unoptimised, insufficient for bots or automated programs. My first time using gitHub so it's a HelloWorld moment. Keep in mind that this program operates on O(n^2) time, where n is the number of words supplied.

The constant ITERDIR contains a number that contains the amount of words the code will evaluate at a time: the program is designed to run a few of the words at a time and save the results. The constant CHECKLEADERBOARD should be set to TRUE if you want to see the results, and LDB_LEN can be changed for how many results you want to see. The constant IGNORE is a list of the sourceword files you specifically do not want the program to access for whatever reasons. The constant DEBUG should be set to TRUE whenever you want to watch the program go fast and run properly.

The .txt files present in the "sourcewords" folder are not my own and have not been collected or collated by me. Any user of this code may add their own .txt files containing lists of words, although note that the code is designed specifically for six-word systems.

The files currently present are attributed as follows:
"5-letter-words.txt" published by daemondevin on gitHub 
"5-letters.txt" published by Blkzer0 on gitHub
"valid-wordle-words" published by dracos on gitHub
"wordle-answers-alphabetical" published by cfreshman on gitHub 

The code will also create a folder within the directory containing the results (2 .txt files): both a list of all words already checked, and the results of their respective expected information gain statistics.

If you're wondering what my results were, it'll take a while but right now the winner is "SLATE"