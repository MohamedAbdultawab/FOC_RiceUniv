# template for "Stopwatch: The Game"
# this project has to be run in codeskulptor.org
# An online version could be found here: www.codeskulptor.org/#user43_ci15x2T36H_0.py

import simplegui

# define global variables
time = 0
num_of_stops = 0
num_of_matches = 0
flag = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t // 600
    seconds = (t % 600)
    if seconds >= 100:
        return '%s:%s' % (str(minutes), str(seconds / 10.0))
    else:
        return '%s:0%s' % (str(minutes), str(seconds / 10.0))


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global flag
    flag = True
    timer.start()


def stop():
    global num_of_stops, num_of_matches, flag
    timer.stop()
    if flag:
        num_of_stops += 1
        if (time % 600) % 10 == 0:
            num_of_matches += 1
    flag = False


def reset():
    global time, num_of_stops, num_of_matches
    timer.stop()
    time = 0
    num_of_stops = 0
    num_of_matches = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1


# define draw handler
def draw(canvas):
    canvas.draw_text(format(time), [180, 110], 18, 'White')
    canvas.draw_text('%d/%d' % (num_of_matches, num_of_stops),
                     [360, 30], 16, 'White')


# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 400, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
start = frame.add_button('Start', start, 100)
stop = frame.add_button('Stop', stop, 100)
reset = frame.add_button('Reset', reset, 100)

# start frame
frame.start()
