# The Perfect Guess
import random as rd

randNumber = rd.randint(0, 100)
# print(randNumber)

userGuess = None
guesses = 0

while userGuess != randNumber:
    
    userGuess = int(input("Guess the number: "))
    guesses += 1
    if userGuess == randNumber:
        print("\nCongrats! You guessed it right.")
    elif userGuess > randNumber:
        print("\nSorry, You guessed it wrong.\nSmaller number please.\n")
    elif userGuess < randNumber:
        print("\nSorry, You guessed it wrong.\nLarger number please.\n")
    
print(f"You got it right in {guesses} guesses.")

with open("highscore.txt", "r") as h:
    existingHi = h.read()

if existingHi == "":
    with open("highscore.txt", "w") as hi:
        hi.write(str(guesses))

elif int(existingHi) > guesses:
    print(f"\nYou have broken the previous high score {existingHi}.\nThe new high score is {guesses}.")
    with open("highscore.txt", "w") as hi:
        hi.write(str(guesses))
