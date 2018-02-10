# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

# Click 'Stop' on whole numbers to earn points

import simplegui

counter = 0
stop_watch = 0
stop_on_whole = 0

def format(t):
    global stop_on_whole
    d = t%10
    q = t/10
    c = q%10
    b = q/10
    a = b/6
    b = b% 6
        
    return str(a)+":"+str(b)+str(c)+"."+str(d)
    
def start():
    global watch_running
    timer.start()
    watch_running = True

def stop():
    global watch_running, stop_watch, stop_on_whole
    if timer.is_running():
        stop_watch += 1
    if (counter%10 == 0 and timer.is_running()):
        stop_on_whole += 1
    timer.stop()
    watch_running = False
    
def reset():
    global counter, watch_running, stop_watch, stop_on_whole
    timer.stop()
    counter = 0
    stop_watch = 0
    stop_on_whole = 0
    watch_running = True

def timer_handler():
    global counter
    counter += 1

def draw(canvas):
    time_in_watch = format(counter)
    canvas.draw_text(time_in_watch,[55,90],40,"White")
    canvas.draw_text(str(stop_on_whole)+"/"+str(stop_watch),[150,25],25,"Red")
    
frame = simplegui.create_frame("Stopwatch",200,200)
frame.add_button("Start",start,75)
frame.add_label(" ")
frame.add_button("Stop",stop,75)
frame.add_label(" ")
frame.add_button("Reset",reset,75)

timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw)

frame.start()
