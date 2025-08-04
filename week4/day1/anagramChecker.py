class AnagramChecker():

    def __init__(self, wordFile = r'C:\Users\emmaf\Documents\Bootcamp\week4\day1\sowpods.txt' ):
        self.wordList = []
        with open (wordFile, 'r') as file:
            for line in file:
                self.wordList.append(line.strip())

    def isValidWord(self, word):
        if word in self.wordList:
            return True
        else:
            return False
        
# get_anagrams(word) – should find all anagrams for the given word. (eg. if word of the user is ‘meat’, the function should return a list containing [“mate”, “tame”, “team”].)
    def getAnagram(self, word):

        anagramPossibilities = []
        anagramList = []

        for item in self.wordList:
            if len(word) == len(item):
                anagramPossibilities.append(item)

        sortedWord = sorted(word)

        for value in anagramPossibilities:
            sortedValue = sorted(value)

            if word != value:
                if sortedWord == sortedValue:
                    anagramList.append(value)

        return anagramList
  
