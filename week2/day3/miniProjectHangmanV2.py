import random

# List of possible words
wordList = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']

# Hangman stages for each wrong guess
hangman_stages = [
    """
--------------
|            |
|            
|            
|            
|            
|
--------------
""",
    """
--------------
|            |
|            O
|            
|            
|            
|
--------------
""",
    """
--------------
|            |
|            O
|            |
|            
|            
|
--------------
""",
    """
--------------
|            |
|            O
|           /|
|            
|            
|
--------------
""",
    """
--------------
|            |
|            O
|           /|\\
|            
|            
|
--------------
""",
    """
--------------
|            |
|            O
|           /|\\
|           / 
|            
|
--------------
""",
    """
--------------
|            |
|            O
|           /|\\
|           / \\
|            
|
--------------
"""
]

# Choose a word randomly from the wordList
def choose_word():
    return random.choice(wordList)

# Display the chosen word
# If guess letter is right, display the letter, else display *
def display_word(word, guessed_letters):
    result = ""
    for letter in word:
        if letter in guessed_letters:
            result += letter + " "
        elif letter == " ":
            result += "  "  # Show space as space
        else:
            result += "* "
    return result.strip()

def play_hangman():
    word = choose_word()
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = len(hangman_stages) - 1

    print("Welcome to Hangman!")
    print(display_word(word, guessed_letters))

    while wrong_guesses < max_wrong:
        print(hangman_stages[wrong_guesses])
        guess = input("Guess a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("Correct!")
        else:
            wrong_guesses += 1
            print("Wrong!")

        current_display = display_word(word, guessed_letters)
        print(current_display)

        if '*' not in current_display:
            print("Congratulations! You guessed the word!")
            break
    else:
        print(hangman_stages[wrong_guesses])
        print(f"You lost! The word was: {word}")

if __name__ == "__main__":
    play_hangman()
