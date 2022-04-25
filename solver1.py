"""
 * 2/22/22 Wordle Solver
 * 
 * Uses Donald Knuth's list of common 5-letter words
 * Makes selections based on the constraints given by the game and 
 * various heuristics, such as letter-frequency score.
 * 
 * Also presents the user with a list of valid words or scored words.
 *
"""

## imports
from utilities import *

#sorry 'y'
vowels = ['a','e','i','o','u']

with open('sgb-words.txt') as f:
    words = f.readlines()

print(len(words))

# remove that pesky newline character.
w1 = [word[0:5] for word in words]

# let's make a new list that filters out words with repeat letters
w2 = [word for word in w1 if has_all_unique_characters(word)]

# get frequency of letters, number of times they appear.
# put into an array. index by character code order
# use ord() method to get ASCII code.
# capital 'A' is 65. lowercase 'a' is 
# I will call a function from another module that does this on a list of strings.
freq_scores = get_letter_frequencies(w1)

print(freq_scores)

positional_scores = get_letter_positional_freqs(w1)
top_scoring_words = sort_words_by_positional_letter_scores(w1, positional_scores, num_words_returned=30)
yellow_scores = get_letter_frequencies(w1)
yellow_top_scoring_words = sort_words_by_letter_scores(w1, yellow_scores)

print("Top scoring words in W1 by green scores")
print(top_scoring_words)
print("Top scoring words in W1 by yellow and green scores")
print(yellow_top_scoring_words)
print()

positional_scores = get_letter_positional_freqs(w1)
top_scoring_words = sort_words_by_positional_letter_scores(w2, positional_scores, num_words_returned=60)
yellow_top_scoring_words = sort_words_by_letter_scores(w2, yellow_scores)

print("Top scoring words in W2, by positional scores from w1")
print(top_scoring_words)
print("Top scoring words in W1 by yellow and green scores")
print(yellow_top_scoring_words)
print()

###################################
# this is where the gaming happens.
###################################
# Do it via a text file.  That's my input.
guesses= []
results= []
# text file format is 
with open("guesses.txt") as g:
    lines = g.readlines()
    for line in lines:
        splits = line.split(",")
        guesses.append(splits[0].strip())
        results.append(splits[1].strip())

game = wordleGame(5)
game.addToWhitelist("")

print("Guesses and Results:")
for i in range(len(guesses)):
    print(guesses[i] + " -- " + results[i])
    game.inform(guesses[i], results[i])
print(game.showColors())
properWords = game.returnProperWords(w1)
print("Complete List of Proper Words")
print(properWords)
print()

positional_scores = get_letter_positional_freqs(properWords)
top_scoring_words = sort_words_by_positional_letter_scores(properWords, positional_scores, num_words_returned=30)
yellow_scores = get_letter_frequencies(w1)
yellow_top_scoring_words = sort_words_by_letter_scores(properWords, yellow_scores)

print("Top scoring proper words, by green scores")
print(top_scoring_words)
print("Top scoring proper words, by yellow scores")
print(yellow_top_scoring_words)
print()

#for word in properWords: 
#    proper_word_scores.append(score_word_by_letters(word, freq_scores))
#top_indices = Nmaxelements(proper_word_scores, 10)

# Not Game, for determining which words are left that don't contain the 
# letters already guessed.
# only the top 15 will be displayed, otherwise SCREEN CLUTTER
notGame = wordleGame(5)
for guess in guesses:
    notGame.addToBlacklist(guess)

# score remaining words based on letter frequency scores in properWords set, above, from 'game'
print("\nPositional Scores:\n")
print(positional_scores)
print("\n")
propers = notGame.returnProperWords(w2)
green_top_scoring_nots = sort_words_by_positional_letter_scores(propers, positional_scores)
yellow_scores = get_letter_frequencies(w1)
yellow_top_scoring_nots = sort_words_by_letter_scores(propers, yellow_scores)
print("Top Scorers from w2 based on green scores")
print(green_top_scoring_nots)
print("Top Scorers from w2 based on yellow scores")
print(yellow_top_scoring_nots)



odd_game = wordleGame(5)
odd_game.addToWhitelist('hpbm')
#odd_game.addToBlacklist('s')
results = odd_game.returnProperWords(w1)
print("Odd Game Results")
print(results)

