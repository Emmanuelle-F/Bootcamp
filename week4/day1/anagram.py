from anagramChecker import AnagramChecker
import re 


def validateWord(word):
    errorMessage = ""

    if ' ' in word:
        errorMessage = "There must be only a single word."

    elif not re.match(r'^[A-Za-z]+$', word):
        errorMessage = "The word must contain only alphabetic letters."

    return errorMessage


word = AnagramChecker()

while True:

    userInput = input('Please enter a word or type quit to exit: ').strip().upper()

    if userInput == "QUIT":
        break

    validationMessage = validateWord(userInput)

    if validationMessage == "":

        if word.isValidWord(userInput):
            anagrams = word.getAnagram(userInput)

            print(f"Word: \"{userInput}\"")
            print(f"Anagrams for the word ({userInput}):", ', '.join(anagrams) if anagrams else "None found.")

        else:
            print(f"The word '{userInput}' is not valid.\n")

