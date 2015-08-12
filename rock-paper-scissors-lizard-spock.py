# Here's my attempt at a Rock-paper-scissors-lizard-Spock game

#library import block
import random

# helper functions block
#convert name string into assigned number
def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    #Data validation, not really necessary
    else:
        print "Name not recognised, try that again."

#convert the assigned number back to the name string
def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
   #This is an error case message, ignore it
    else:
        print "Yo, the number_to_name function has sprung a leak."
    
#main function body
def rpsls(player_choice): 
    print ""
    print "Player chooses " + player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + comp_choice
    difference = (comp_number - player_number) % 5
    if difference == 0:
        print "Player and computer tie!"
    elif difference < 3:
        print "Computer wins!"
    else:
        print "Player wins!"        
    
# Code test block
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")