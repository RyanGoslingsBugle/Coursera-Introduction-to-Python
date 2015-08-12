# requires SimpleGUICS2Pygame module

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# global variables

secret_number = 0
secret_range = 101
allowed_guesses = 7

# helper functions
def new_game():
    global secret_number, secret_range, allowed_guesses
    secret_number = random.randrange(0, secret_range)
    allowed_guesses = int(math.ceil(math.log(secret_range,2)))
    print "Computer has picked a number between 0 and " + str(secret_range-1)
    print "Enter your number."
    print "Guesses left: " +str(allowed_guesses)

# define event handlers
def range100():
    global secret_range
    secret_range = 101
    new_game()
  
def range1000():
    global secret_range
    secret_range = 1001
    new_game()
    
def input_guess(guess):
    global secret_number, allowed_guesses
    player_guess = float(guess)
    print
    print "You guessed " + guess
    if player_guess == secret_number:
        print
        print "That's it, you got it!"
        new_game()
    elif player_guess > secret_number:
        allowed_guesses = allowed_guesses - 1 
        print
        print "Lower!"
        print "Guesses left: " +str(allowed_guesses)
    else:
        allowed_guesses = allowed_guesses - 1
        print
        print "Higher!"
        print "Guesses left: " +str(allowed_guesses)
    if allowed_guesses == 0:
        print
        print "Sorry, better luck next time."
        new_game()
    
# create frame

frame = simplegui.create_frame("Main frame",200,200)

# register event handlers

range1 = frame.add_button("Range 0-100",range100,100)
range2 = frame.add_button("Range 0-1000",range1000,100)
guess = frame.add_input("Guess:",input_guess,200)

# start statement

new_game()

# Here's a little test to see if you read this far
# Leave the answer in the evaluation comments
# What were Mr. Spock's last words to Jim Kirk before his death?