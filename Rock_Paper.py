# Rock-paper-scissors-lizard-Spock template

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


# print(number_to_name(1), name_to_number('Spock'))
# print(number_to_name(4), name_to_number('scissors'))
# print(number_to_name(5), name_to_number('spock'))


def rpsls(player_choice):
    # delete the following pass statement and fill in your code below

    # print a blank line to separate consecutive games
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

    # print out the message for the player's choice

    # compute random guess for comp_number using random.randrange()

    # convert comp_number to comp_choice using the function number_to_name()

    # print out the message for computer's choice

    # compute difference of comp_number and player_number modulo five

    # use if/elif/else to determine winner, print winner message


# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
