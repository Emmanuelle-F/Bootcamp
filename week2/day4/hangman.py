import random

NUMBER_TRIALS = 6
wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']

def showChanges(guessedWord):
    for word in guessedWord:
        print (word)

def gameFlow():
    currentTrial = 0
    guessedLetters = []
    guessedWord = []

    selectedWord = random.choice(wordslist) 

    print("Welcome to Hangman!")

    for i in selectedWord:
        guessedWord.append("-")

    while currentTrial < NUMBER_TRIALS:
        showChanges(guessedWord)



    
    


gameFlow()
