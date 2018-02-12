# implementation of card game - Memory
# this project has to be run in codeskulptor.org
# An online version could be found here: http://www.codeskulptor.org/#user43_KAszBvZ5St_0.py

import simplegui
import random

card1 = None
card1_index = None
card2 = None
card2_index = None

# helper function to initialize globals


def pos_to_index(pos):

    if pos[0] < 60:
        return 0
    elif pos[0] < 120:
        return 1
    elif pos[0] < 180:
        return 2
    elif pos[0] < 240:
        return 3
    elif pos[0] < 300:
        return 4
    elif pos[0] < 360:
        return 5
    elif pos[0] < 420:
        return 6
    elif pos[0] < 480:
        return 7
    elif pos[0] < 540:
        return 8
    elif pos[0] < 600:
        return 9
    elif pos[0] < 660:
        return 10
    elif pos[0] < 720:
        return 11
    elif pos[0] < 780:
        return 12
    elif pos[0] < 840:
        return 13
    elif pos[0] < 900:
        return 14
    elif pos[0] < 960:
        return 15


def new_game():
    global counter, state, cards_list, exposed
    counter = 0
    label.set_text('Turns = ' + str(counter))
    state = 0
    cards_list = list(range(8))
    random.shuffle(cards_list)
    cards_list = cards_list + cards_list
    random.shuffle(cards_list)
    exposed = [False for i in range(16)]


# define event handlers
def mouseclick(pos):
    global state, card1, card1_index, card2, card2_index, counter

    index = pos_to_index(pos)
    if not exposed[index]:

        exposed[index] = True
        if state == 0:
            state = 1
            card1 = cards_list[index]
            card1_index = index
        elif state == 1:
            counter += 1
            label.set_text('Turns = ' + str(counter))
            state = 2
            card2 = cards_list[index]
            card2_index = index
        elif state == 2:
            state = 1
            if card1 != card2:
                exposed[card1_index] = False
                exposed[card2_index] = False
            card1 = cards_list[index]
            card1_index = index


# cards are logically 50x100 pixels in size
def draw(canvas):
    for i, v in enumerate(cards_list):
        if exposed[i]:
                canvas.draw_polygon([[i * 60, 0],
                                     [i * 60 + 60, 0],
                                     [i * 60 + 60, 100],
                                     [i * 60, 100]],
                                    6,
                                    'White',
                                    'Black')
                canvas.draw_text(str(v), [i * 60 + 25, 57], 15, 'White')
        else:
                canvas.draw_polygon([[i * 60, 0],
                                     [i * 60 + 60, 0],
                                     [i * 60 + 60, 100],
                                     [i * 60, 100]],
                                    6,
                                    'White',
                                    'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 960, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
