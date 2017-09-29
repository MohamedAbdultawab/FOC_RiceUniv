# Rock-paper-scissors-lizard-Spock
# this project has to be run in codeskulptor.org
# An online version could be found here: http://www.codeskulptor.org/#user43_3gGRNpuZM6iBOVp.py

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

from random import randrange


def name_to_number(name):

    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print("The name you entered isn't valid")


def number_to_name(number):

    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print("The number you entered isn't valid")


def rpsls(player_choice):
   
    print('\n')
    print('Player chooses ' + player_choice)

    player_number = name_to_number(player_choice)
    comp_number = randrange(0, 5)
    comp_choice = number_to_name(comp_number)

    print('Computer chooses ' + comp_choice)

    diff_player_and_comp = (comp_number - player_number) % 5

    if diff_player_and_comp == 0:
        print('Player and Computer ties!')
    elif diff_player_and_comp == 1 or diff_player_and_comp == 2:
        print('Computer wins!')
    elif diff_player_and_comp == 3 or diff_player_and_comp == 4:
        print('Player wins!')
    else:
        print('There was an error!')


# tests
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
