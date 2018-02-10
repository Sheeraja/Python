# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

# For the player on the left, 'w' moves the paddle up and 's' moves it down
# For the player on the right, 'up' arrow moves the paddle up and 'down' arrow moves it down

import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = (WIDTH/2,HEIGHT/2)
ball_vel = [1,-1]

paddle1_pos = HEIGHT / 2.5
paddle2_pos = HEIGHT / 2.5

paddle_vel = 5
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

ball_vel = [0,0]
ball_pos = [WIDTH/2, HEIGHT/2]

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel = [1,0]
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction:
        ball_vel = [random.randrange(2,4), -random.randrange(1, 3)]
    elif not direction:
        ball_vel = [-random.randrange(2,4), -random.randrange(1, 3)]

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]  
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    
    if paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    if paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                     [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "Yellow")
    
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "Yellow")
    
    if ball_pos[0] == PAD_WIDTH + BALL_RADIUS and ball_pos[1] in range(paddle1_pos - (HALF_PAD_HEIGHT+BALL_RADIUS), paddle1_pos + (HALF_PAD_HEIGHT+BALL_RADIUS)):
        ball_vel[0] = -ball_vel[0]
    
    elif ball_pos[0] == WIDTH - (PAD_WIDTH + BALL_RADIUS) and ball_pos[1] in range(paddle2_pos - (HALF_PAD_HEIGHT+BALL_RADIUS), paddle2_pos + (HALF_PAD_HEIGHT+BALL_RADIUS)):
        ball_vel[0] = -ball_vel[0]
        
    if ball_pos[0] > WIDTH - (BALL_RADIUS+PAD_WIDTH):
        score1 += 1
        spawn_ball(LEFT)
    elif ball_pos[0] < 0 + (BALL_RADIUS+PAD_WIDTH):
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] <= 0 + BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    canvas.draw_text(str(score1), [WIDTH // 3, HEIGHT // 4], 40, "Red")
    canvas.draw_text(str(score2), [2 * WIDTH // 3, HEIGHT // 4], 40, "Red")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle_vel
    global paddle1_pos, paddle2_pos
    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_vel
  
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -paddle_vel
    
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle_vel
  
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -paddle_vel   

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]: 
        paddle1_vel = 0

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

new_game()
frame.start()
