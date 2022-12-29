def get_letter_frequencies(words):
    freqs = [0 for i in range(26)]
    for word in words:
        # let's assume the words are pre-sorted and lowercased.
        #word = word.lower()
        for l in word:
            if is_valid_character(l):
                index = ord(l) - 97 
                freqs[index] += 1
    return freqs


def score_word_by_letters(word, letter_scores):
    score = 0
    for l in word:
        if is_valid_character(l):
            score += letter_scores[ord(l) - 97]

    return score

# be careful! I am using the raw positional score dictionary returned by get_letter_positional_freqs
# this format is {'letter': [total_count, [pos1, pos2, pos3, pos4, pos5]]}.  So freqs[letter][1] is our positional count array.
def sort_words_by_positional_letter_scores(words, positional_scores, num_words_returned=15, descending=True):
    scores = [0 for i in range(len(words))]
    for i in range(len(words)):
       score = 0
       for j in range(len(words[i])):
           l = words[i][j]
           if is_valid_character(l):
               if l not in positional_scores.keys():
                   score += 0
               else:
                   score += positional_scores[l][1][j]
       scores[i] = score

    # make sure we aren't returning more words than are in the words parameter
    # we'll go out of bounds of the words list otherwise--that's a python error
    # in that case just return the entire list, sorted.
    if num_words_returned > len(words):
        num_words_returned = len(words)

    top_indices = Nmaxelements(scores, num_words_returned)
    top_scoring_words = list()
    
    for i in range(len(top_indices)):
        top_scoring_words.append(words[top_indices[i]])

    return top_scoring_words



def sort_words_by_letter_scores(words, letter_scores, num_words_returned=15, descending=True):
    scores = [0 for i in range(len(words))]
    for i in range(len(words)):
       score = 0
       for l in words[i]:
           if is_valid_character(l):
               score += letter_scores[ord(l) - 97]
       scores[i] = score

    # make sure we aren't returning more words than are in the words parameter
    # we'll go out of bounds of the words list otherwise--that's a python error
    # in that case just return the entire list, sorted.
    if num_words_returned > len(words):
        num_words_returned = len(words)

    top_indices = Nmaxelements(scores, num_words_returned)
    top_scoring_words = list()
    
    for i in range(len(top_indices)):
        top_scoring_words.append(words[top_indices[i]])

    return top_scoring_words


        
def is_valid_character(l):
    return ord(l) > 96 and ord(l) < 123


def Nmaxelements(list1, N):
    index_list = []

    # don't want a segfault! (not that you can in python)
    if len(list1) < N:
        N = len(list1)
  
    for i in range(0, N): 
        max1 = 0
        max1index = 0
          
        for j in range(len(list1)):     
            if list1[j] > max1:
                if j not in index_list:
                    max1 = list1[j];
                    max1index = j

        index_list.append(max1index)

    return index_list

def has_all_unique_characters(word):
    letters = list()
    for letter in word:
        if is_valid_character(letter):
            if letter in letters:
                return False
            else:
                letters.append(letter)
    return True

# obtain a list of positional frequencies for each letter for a given list of words.
# the words must be five letters long.
# provided information? count of letter in word list, and count of positional occurence.
def get_letter_positional_freqs(words):
    info = {}
    for word in words:
        for i in range(len(word)):
            letter = word[i]
            if is_valid_character(letter):
                if letter not in info.keys():
                    info[letter] = [0, [0 for i in range(5)]]
                try:
                    info[letter][0] += 1
                    info[letter][1][i] += 1
                except:
                    print("word, letter:")
                    print(word + ", " + letter)
    return info



class wordleGame:

    def __init__(self, length):
        self.blacklist = []     # letters that ARE NOT in the word
        self.whitelist = []     # letters that MAY BE in the word -- useful for filtering long lists
        self.colors = {}        # letters with positional information
        self.length = length    # the length of the word to target

    # takes in a set of words and returns valid choices from them
    # according to the blacklist and colors information
    def returnProperWords(self, words):
        properWords = []
        for word in words:

            # check for properness 
            proper = True
            if len(word) != self.length:
                proper = False
                continue

            for letter in self.whitelist:
                proper = False
                for l in word:
                    if l == letter:
                        proper = True
                if not proper:
                    break

                

            for letter in self.blacklist:
                if letter in word:
                    proper = False
                    break
            if not proper:
                continue 

            # check to see if it has all of the letters required.
            for letter in self.colors:
                if letter not in word:
                    proper = False
                    break
            if not proper:
                continue

            # now check for positional requirements.
            for letter in self.colors:
                for i in range(self.length):
                    if self.colors[letter][i] == 'y':
                        if word[i] == letter:
                            proper = False
                            break
                    if self.colors[letter][i] == 'g':
                        if word[i] != letter:
                            proper = False
                            break
                if not proper:
                    break

            if proper:
                properWords.append(word)

        return properWords



    def showColors(self):
        print("Colors:")
        print(self.colors)
        print("Blacklist:")
        print(self.blacklist)
        print("Whitelist:")
        print(self.whitelist)




    # Insert information returned from the game about letters.
    # takes the word guessed (guess) and the information returned (result)
    # both should be STRINGs of equal length
    # information encoded is trinary--black, yellow, green, or 'b', 'y', 'g'.
    # EXAMPLE: guess="trove", return="bgbby"
    def inform(self, guess, result):
        if len(guess) != len(result):
            return -1
        guess = guess.lower()
        result = result.lower()
        for i in range(len(guess)):
            if result[i] == 'b':
                # for now, I don't care if we have repeat values.
                # it won't change the returnProperWords algorithm.
                # plus, you can check to see if you guessed with a black letter. Shame!
                # if result[i] not in self.blacklist
                self.blacklist.append(guess[i])

            # same effect for yellows and greens.
            # this works even if the information has already been entered in that position.
            if result[i] == 'y' or result[i] == 'g':
                # check if the letter entry already exists.
                if guess[i] in self.colors.keys():
                    # somehow update the entry for that letter.
                    # this involves setting the characters of a five letter string.
                    # since strings are immutable in python, let's just make the 
                    # information a list.
                    self.colors[str(guess[i])][i] = result[i]
                else:
                    # create an entry in the self.colors dictionary for that letter.
                    self.colors[guess[i]] = ['' for i in range(self.length)]
                    # then update the position i with the color information 
                    self.colors[str(guess[i])][i] = result[i]
        # cleanup blacklist
        for i in range(len(guess)):
            if guess[i] in self.blacklist and (result[i] == 'g' or result[i] == 'y'):
                # this only removes the first instance of the letter in the blacklist.
                # it's probably OK. The letter shouldn't be in there more than once.
                # SHOULDN'T
                # but then I added the 'addToBlacklist' method, after this comment. Just so that it COULD
                self.blacklist.remove(guess[i])
                    
    # add letters to the whitelist.
    # these letters are used to determine the properness of a word in 
    # the returnProperWords method.
    # A word is proper only IF if includes all these letters.
    # useful for searching for words that have a specific letter you would like 
    # to guess with.
    # No positional information is associated with these letters.
    # These letters are 'assumptions' of the target word.
    def addToWhitelist(self, letters):
        for letter in letters:
            self.whitelist.append(letter)

    # clears the whitelist.
    # this removes the constraints it enforces on filtering.
    # White letters are only assumptions 
    def clearWhitelist(self):
        self.whitelist.clear()

    def addToBlacklist(self, letters):
        for letter in letters:
            self.blacklist.append(letter)

    def clearBlacklist(self):
        self.blacklist.clear()

    # adds an entry to the colors list, one letter at a time.
    # This is different from inform because it does one letter at a time,
    # which requires positional information to be given.
    def addColor(self, letter, color, index):
        if color in self.colors.keys():
            self.colors[str(letter)][index] = color
        else:

            self.colors[str(letter)] = ['' for i in range(self.length)]
            self.colors[str(letter)][index] = color
