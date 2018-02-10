# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(ship_image,[45,45], [90,90], self.pos, [90,90], self.angle)

    def update(self):
        self.angle += self.angle_vel
        
        if self.thrust:
            acceleration = angle_to_vector(self.angle)
            self.vel[0] += acceleration[0] * 0.3
            self.vel[1] += acceleration[1] * 0.3
        
        self.vel[0] *= 1 - 0.05
        self.vel[1] *= 1 - 0.05        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
    
    def rotate(self, direction):
        if direction == "left":
            self.angle_vel = -0.05
        elif direction == "right":
            self.angle_vel = 0.05
        elif direction == "stop":
            self.angle_vel = 0
        
    def move(self, move):
        self.thrust = move
        if move:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile
        
        missile_pos = [self.pos[0] + angle_to_vector(self.angle)[0] * self.image_size[0] / 2, 
                       self.pos[1] + angle_to_vector(self.angle)[1] * self.image_size[1] / 2]
        missile_vel = [self.vel[0] + angle_to_vector(self.angle)[0] * 2, 
                       self.vel[1] + angle_to_vector(self.angle)[1] * 2]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
           
    def draw(self,canvas):
        if self.thrust:
            thrust_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, thrust_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT       

           
def draw(canvas):
    global time
    
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    canvas.draw_text("Lives: "+str(lives),[50,25],20,"White")
    canvas.draw_text("Score: "+str(score),[700,25],20,"White")
            
def key_down(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate("left")
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate("right")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.move(True)    
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def key_up(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.rotate("stop")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.move(False)

def rock_spawner():
    global a_rock
    
    pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    vel = [random.choice([-1, 1]) * random.randint(0, 5), random.choice([-1, 1]) * random.randint(0,5)]
    angle = random.random() * 2 * math.pi
    angle_vel = random.choice([-1, 1]) * random.random() * 0.05
        
    a_rock = Sprite(pos, vel, angle, angle_vel, asteroid_image, asteroid_info)
    
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

frame.set_draw_handler(draw)
frame.set_keyup_handler(key_up)
frame.set_keydown_handler(key_down)
timer = simplegui.create_timer(1000.0, rock_spawner)

timer.start()
frame.start()