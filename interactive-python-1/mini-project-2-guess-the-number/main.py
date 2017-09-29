# Guess the number
# this project has to be run in codeskulptor.org
# An online version could be found here: www.codeskulptor.org/#user43_kgdfsZQwe8_1.py
# input will come from buttons and an input field
# all output for the game will be printed in the console

from random import randrange
import simplegui

secret_num = None
num_of_guesses = 7
num_range = 100


# helper function to start and restart the game
def new_game():
    global secret_num, num_of_guesses, num_range
    secret_num = randrange(0, num_range)
    num_of_guesses = 7 if num_range == 100 else 10
    print('New game started, with range ' +
          str(num_range) + ' and ' + str(num_of_guesses) + ' guesses')
    print('')


# event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global num_range
    num_range = 1000
    new_game()


def input_guess(guess):
    # main game logic goes here
    global secret_num, num_of_guesses, num_range

    print('Guess was ' + guess)

    guess = int(guess)

    if guess >= 0 and guess <= num_range:
        if guess > secret_num:
            print('Higher')
        elif guess < secret_num:
            print('Lower')
        else:
            print('Correct')
            print('')
            new_game()
            return

        num_of_guesses -= 1
        if num_of_guesses == 0:
            print('')
            print('Game Over')
            print('')
            new_game()
            return
        print('')
        print('you have ' + str(num_of_guesses) + ' guesses left')
    else:
        print('Your guess is out of range')
        print('')
        print('you have ' + str(num_of_guesses) + ' guesses left')


# create frame
frame = simplegui.create_frame('Guess the Number', 200, 200)

# register event handlers for control elements and start frame
inp = frame.add_input('Enter your guess', input_guess, 50)
range_100 = frame.add_button('Range {0, 100)', range100)
range_1000 = frame.add_button('Range {0, 1000)', range1000)

# call new_game
new_game()

frame.start()
