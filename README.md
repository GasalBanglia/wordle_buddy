# wordle_buddy
A set of utility functions and a class that use a dictionary of 5-letter words to help you decide which words to guess in Wordle. 

Their primary function is filtering the dictionary into 'legal' subsets of valid words (based on the color information) and ranking those words based on letter frequencies.

The dictionary was taken from Donald Knuth's webpage. He is a retired professor at Stanford. His webpage is here: https://www-cs-faculty.stanford.edu/~knuth/. 
The dictionary is not complete, containing less than half of the 5-letter words recognized by the English language. For the New York Times Wordle, however, it is more than sufficient. 
