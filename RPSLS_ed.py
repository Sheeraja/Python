# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

# Game - Rock Paper Scissors Lizard Spock

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors


import random

def name_to_number(name):
    if name == 'rock' or name == 'Rock':
        return 0
    elif name == 'spock' or name == 'Spock':
        return 1
    elif name == 'paper' or name == 'Paper':
        return 2
    elif name == 'lizard' or name == 'Lizard':
        return 3
    elif name == 'scissors' or name == 'Scissors':
        return 4
    else:
        return 'Invalid input'

def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return 'Invalid input'    

def rpsls(player_choice): 
    print " "
    print "Player chooses "+player_choice
    player_number = name_to_number(player_choice)
    
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses "+comp_choice
    
    diff = (comp_number - player_number) % 5
    
    if diff == 1 or diff == 2:
        print "Computer wins!"
    elif diff == 3 or diff == 4:
        print "Player wins!"
    else:
        print "Player and Computer tie!"
