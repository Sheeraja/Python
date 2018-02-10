# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

import simplegui
import random
import math

# initialize global variables
secret_number = 0
num_range = 100
guesses = 7

# start and restart the game
def new_game():
    global secret_number, num_range, guesses
    secret_number = random.randrange(0,num_range)
    guesses = int(math.ceil(math.log(num_range - 0 + 1)/math.log(2)))
    print "\nNew Game. Range is from 0 to " + str(num_range)
    print "Number of remaining guesses is " + str(guesses)

# event handlers
def range100():
    global num_range
    num_range = 100
    new_game()

def range1000():
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    global guesses, num_range
    guesses -= 1
    number_guessed = int(guess)
    print "\nGuess was "+str(number_guessed) + "\nNumber of remaining guesses is ",guesses
    if (guesses == 0 and number_guessed != secret_number):
        print "You ran out of guesses. The number was " + str(secret_number)
        new_game()
    else:
        if number_guessed > secret_number:
            print "Lower!"
        elif number_guessed < secret_number:
            print "Higher!"
        else:
            print "Correct!"
            new_game()
    
f = simplegui.create_frame("Guess the Number!!",200,200)
f.add_button("Range is [0,100)",range100)
f.add_button("Range is [0,1000)",range1000)
f.add_input("Enter Number: ",input_guess,100)

f.start()

new_game()
