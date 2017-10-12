# Implementation of classic arcade game Pong

# this project has to be run in codeskulptor.org
# An online version could be found here: http://www.codeskulptor.org/#user43_IDomfjjMX3_0.py

import simplegui
from random import randrange

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = (HEIGHT - PAD_HEIGHT) / 2
paddle2_pos = (HEIGHT - PAD_HEIGHT) / 2
paddle1_vel = 0
paddle2_vel = 0
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction:
        ball_vel = [randrange(2, 4), -1 * randrange(1, 3)]
    else:
        ball_vel = [-1 * randrange(2, 4), -1 * randrange(1, 3)]


# define event handlers
def new_game():
    # these are numbers
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle2_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],
                     [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] *= -1
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, 'White', 'White')
    # Collisions
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos and \
           ball_pos[1] <= paddle1_pos + PAD_HEIGHT:

            ball_vel[0] = ball_vel[0] + (ball_vel[0] * .1)
            ball_vel[1] = ball_vel[1] + (ball_vel[1] * .1)
            ball_vel[0] *= -1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] >= paddle2_pos and\
           ball_pos[1] <= paddle2_pos + PAD_HEIGHT:

            ball_vel[0] = ball_vel[0] + (ball_vel[0] * .1)
            ball_vel[1] = ball_vel[1] + (ball_vel[1] * .1)
            ball_vel[0] *= -1
        else:
            score1 += 1
            spawn_ball(LEFT)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel > 0 and\
       paddle1_pos + paddle1_vel < HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    canvas.draw_polygon([[0, paddle1_pos],
                         [PAD_WIDTH, paddle1_pos],
                         [PAD_WIDTH, paddle1_pos + PAD_HEIGHT],
                         [0, paddle1_pos + PAD_HEIGHT]],
                        2, 'White', 'White')
    if paddle2_pos + paddle2_vel > 0 and\
       paddle2_pos + paddle2_vel < HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    canvas.draw_polygon([[(WIDTH - PAD_WIDTH), paddle2_pos],
                         [WIDTH, paddle2_pos],
                         [WIDTH, paddle2_pos + PAD_HEIGHT],
                         [(WIDTH - PAD_WIDTH), paddle2_pos + PAD_HEIGHT]],
                        2, 'White', 'White')
    # draw paddles

    # draw scores
    canvas.draw_text(str(score1), [75, 35], 20, 'White')
    canvas.draw_text(str(score2), [WIDTH - 75, 35], 20, 'White')


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 3
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 3


def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel, paddle2_vel = 0, 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)

# start frame
new_game()
frame.start()
