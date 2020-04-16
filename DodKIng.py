import pygame
import random
import math
import time
import threading
from collections import Iterable
try:
    from shapes import Ball
except ImportError:
    from .shapes import Ball


# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
SKY = (143,203,239)
PINK = (255,20,147)

# Buttons
LEFT = 1
SCROLL = 2

RIGHT = 3
# Images path'
IMAGE = r'/home/yonatan/Documents/Python/pictures/madagascar_1.jpg'
PLANE = r'/home/yonatan/Documents/Python/pictures/plane.png'
BULLET = r'/home/yonatan/Documents/Python/pictures/bullet.png'
SOUND_FILE_AFTER_KING = r'/home/yonatan/Documents/Python/sounds/HailToTheKing.mp3'
SOUND_FILE_BEFORE_KING = r'/home/yonatan/Documents/Python/sounds/moveit.mp3'
SOUND_FILE_BULLET = '/home/yonatan/Documents/Python/sounds/gun_shot.mp3'
REFRESH_RATE = 60
ZERO = 0
NUMBER_OF_BALLS = 50
DISTANCE = 15
RADIUS = 50
SPEED = 15
KING_EXIST = False
RIGHT_CLICK = False
DOWN = True
MIN_RAD = 45
MAX_RAD = 150
HAIL_TO_THE_KING = pygame.mixer.Sound
BULLET_SPEED = 25
no_bullets = True

# Make Sound run in loops
#def play(sound, start, end):
    #sound.set_pos(start)
    #sound.play()
    #time.sleep(end - start)     # in seconds
    #sound.stop()
    #return True

# Vars
global balls_not_in_place
balls_not_in_place = True
finish = False
add_to_angle = 0
mouse_point_list = []
shot = False
timer_list = []

############### Initialization ##############
# Init screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

# Add img to screen
img = pygame.image.load(IMAGE)

# Sound effect
pygame.mixer.init()

# Add clock
clock = pygame.time.Clock()

# Add Plane
player_image = pygame.image.load(PLANE).convert()
player_image.set_colorkey(PINK)

# Bullet
bullet_image = pygame.image.load(BULLET).convert()
bullet_image.set_colorkey(PINK)


# Create a ball list
ball_list = pygame.sprite.Group() # Create a list of objects
new_ball_list = pygame.sprite.Group() # Create a list of objects
bullet_list = pygame.sprite.Group() # Create a king list
'''
for i in range(NUMBER_OF_BALLS):
    ball = Ball(i* DISTANCE, i*DISTANCE)
    ball_list.add(ball)
ball_list.draw(screen)
'''


############### FUNCTIONS ###############
def debug(whatever):
    print(whatever)
    return

# Random speed cant be 0
def rnd_speed():
    speed = random.randrange(-7,7)
    if speed == 0:
        speed = rnd_speed()
    return speed

# Create a random king ball
def king_math():
    num = random.randrange(0,1000)
    return num == 7

# Add a ball object
def add_ball_to_board(x,y):
    global RIGHT_CLICK
    global KING_EXIST
    if not KING_EXIST: # Stopes adding balls when the king is here
        if RIGHT_CLICK:
            isKING = True
        else:
            isKING = king_math()
        ball = Ball(x, y, isKING)
        if ball.is_king():
            #music = pygame.mixer_music
            #sound = music.load(SOUND_FILE_AFTER_KING)
            #sound_thread = threading.Thread(target=play, args=([sound, 1, 2]))
            #sound_thread.start()

            pygame.mixer_music.load(SOUND_FILE_AFTER_KING)
            pygame.mixer_music.play()
            vx = 0
            vy = 0
            ball.update_v(vx, vy)
            global KING_POS
            KING_EXIST = True
            global king_ball
            king_ball = ball # Saves the king ball object
            KING_POS = king_ball.get_pos() # Saves the king ball position
        else:
            vx = rnd_speed()
            vy = rnd_speed()
            ball.update_v(vx, vy)
        ball_list.add(ball)

# Sum of balls
def count_balls(balls_list):
    num_of_balls = 0
    for ball in balls_list:
        num_of_balls += 1
    return num_of_balls -1



# Create array with circle positions
def create_king_circle(num_of_balls, move_with_king = False):
    global DOWN
    global MIN_RAD
    global MAX_RAD
    global add_to_angle
    global RADIUS
    global king_ball
    global SPEED
    SPEED = num_of_balls


    circle_pos_list = []
    X1, Y1 = king_ball.get_pos()
    for angle in range(0, 360, int(360/(num_of_balls))):
        if move_with_king:
            if num_of_balls == 1:
                add_to_angle += 10.8
            else:
                add_to_angle += math.pi / SPEED
            angle += add_to_angle


        X2 = X1 + (math.cos(math.radians(angle)) * RADIUS)
        Y2 = Y1 + (math.sin(math.radians(angle)) * RADIUS)
        cir_pos = (X2,Y2)
        circle_pos_list.append(cir_pos)
    # Makes dod go in and out
    if RADIUS == MAX_RAD:
        DOWN = True
    elif RADIUS == MIN_RAD:
        DOWN = False
    if DOWN:
        RADIUS -= 1
    else:
       RADIUS += 1


    return circle_pos_list

# Change ball speed to match pos
def change_speed_to_pos( ball, ball_x, ball_y, pos_x, pos_y):
    if pos_x > (ball_x + 3):
        vx = 3
    elif pos_x < (ball_x - 3):
        vx = -3
    else:
        vx = 0
        ball.set_pos(pos_x, ball_y)
    if pos_y > (ball_y + 3):
        vy = 3
    elif pos_y < (ball_y - 3):
        vy = -3
    else:
        vy = 0
        ball.set_pos(ball_x, pos_y)
    return vx, vy

# Moves all balle's towards the king ball
def go_to_pos():
    global king_ball
    index = 0
    ball_count = count_balls(ball_list)
    circle_pos_list = create_king_circle(ball_count)
    for ball in ball_list:
        if not ball.is_king():
            if index < len(circle_pos_list):
                pos_x, pos_y = circle_pos_list[index]
            x, y = ball.get_pos()
            vx, vy = change_speed_to_pos(ball, x, y ,pos_x, pos_y)
            if vx == 0 and vy == 0: # Check if the ball has got to position
                ball_count -= 1
            ball.update_v(vx,vy)
            ball.update_loc()
            index += 1
    if ball_count == 0:
        global balls_not_in_place
        balls_not_in_place = False
        vx = rnd_speed()
        vy = rnd_speed()
        king_ball.update_v(vx, vy)

def change_to_pos():
    global king_ball
    index = 0
    ball_count = count_balls(ball_list)
    circle_pos_list = create_king_circle(count_balls(ball_list), True)
    for ball in ball_list:
        if not ball.is_king():
            if index < len(circle_pos_list):
                pos_x, pos_y = circle_pos_list[index]
            ball.set_pos(pos_x, pos_y)
            vx, vy = 0, 0
            ball.update_v(vx, vy)
            ball.update_loc()
            index += 1

# Stops all balls
def stop_all_balls():
    for ball in ball_list:
        ball.update_v(0,0)

def dont_touch_corners(ball_list):
    if isinstance(ball_list, Iterable):
        for ball in ball_list:
            ball.update_loc()
            x, y = ball.get_pos()
            if x > WINDOW_WIDTH - 1 or x < 1:
                vx, vy = ball.get_v()
                ball.update_v(-vx, vy)
            if y > WINDOW_HEIGHT - 1 or y < 1:
                vx, vy = ball.get_v()
                ball.update_v(vx, -vy)


    else: # If this is the king ball
        ball_list.update_loc()
        x, y = ball_list.get_pos()
        if x > WINDOW_WIDTH - 1 or x < 1:
            vx, vy = ball_list.get_v()
            ball_list.update_v(-vx, vy)
        if y > WINDOW_HEIGHT - 1 or y < 1:
            vx, vy = ball_list.get_v()
            ball_list.update_v(vx, -vy)

def ball_colliosion(ball_list, king_list):
    new_ball_list.empty()
    for ball in ball_list:
        ball_hit_list = pygame.sprite.spritecollide(ball, king_list, False)
        if len(ball_hit_list) == 0:
            new_ball_list.add(ball)
        ball_list.empty()
        for ball in new_ball_list:
                ball_list.add(ball)
    return ball_list


# Action's after king ball is created
def the_king_is_here():
    stop_all_balls()
    # debug(len(create_king_circle(count_balls(ball_list))))
    #    debug(create_king_circle(count_balls(ball_list)))
    go_to_pos()

def move_in_arch(pos_x, pos_y):
    speed = 3
    angle = 1
    velocity_y = -1
    velocity_x = 1
    pos_x += velocity_x
    pos_y += velocity_y
    return  pos_x, pos_y

def king_is_moving():
    change_to_pos()


def continue_board(pre_king):
    if pre_king:
        dont_touch_corners(ball_list)

    else:
        global king_ball
        dont_touch_corners(king_ball)
def shot_bullet():
    mouse_point_list.append(pygame.mouse.get_pos())
    #pygame.mixer_music.load(SOUND_FILE_BULLET)
    #pygame.mixer_music.play()

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            RIGHT_CLICK = True
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: # and not KING_EXIST
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)
            if len(ball_list) == 1:
                pygame.mixer_music.load(SOUND_FILE_BEFORE_KING)
                pygame.mixer_music.play()
            if shot:
                shot_bullet()


    if KING_EXIST and balls_not_in_place:
        the_king_is_here()
    elif KING_EXIST and not balls_not_in_place:
        continue_board(False)
        king_is_moving()

        # Remove mouse point
        pygame.mouse.set_visible(False)

        # Add Plane to game
        mouse_point = (pygame.mouse.get_pos())
        screen.blit(player_image, mouse_point)
        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            shot = True
            no_bullets = False
            if (no_bullets):
                shot_bullet()
        if shot:
            for index in range(0, len(mouse_point_list), 1):
                timer_list.append(ZERO)  # Create a bullet starting time
                index_time = timer_list[index]
                posion = mouse_point_list[index]  # Bullet starting posion
                bullet_x_pos = posion[0]
                bullet_y_pos = posion[1]

                bullet_x_pos += index_time  # Move the bullet with time
                index_time += BULLET_SPEED # Time passing..
                (bullet_image, [bullet_x_pos, bullet_y_pos])
                del timer_list[index]  # Edit bullet time
                timer_list.insert(index, index_time)

                screen.blit(bullet_image, [bullet_x_pos, bullet_y_pos])
        screen.blit(player_image, mouse_point)
        pygame.display.flip()



    else:
        continue_board(True)
    screen.blit(img, (0, 0))
    ball_list.draw(screen)
    pygame.display.flip()
    clock.tick(REFRESH_RATE)