from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

DIR_NONE = 0
DIR_LEFT = 1
DIR_RIGHT = 2


game = game_base()
l_s = '00000000000000200000000000000000'
r_s = '00000000000000002000000000000000'
b_s = '0000000000ff00000000ff0000000000'

left_h = sprite_create(l_s)
game.add_sprite(left_h)
right_h = sprite_create(r_s)
game.add_sprite(right_h)

game.set_background(b_s)
game.game_start()

move_lock_flag = False
speed = 10
score = 0

bg_change_count = 0

# default speed 3
def speed_control():
    global speed
    speed = codey.dail() // 5
    print(speed)

def move_control():
    global speed, move_lock_flag

    if codey.is_button('A') and move_lock_flag == False:
        left_h.set_position([-1, 0])
    else:
        left_h.home()
    if codey.is_button('B') and move_lock_flag == False:
        right_h.set_position([1, 0])
    else:
        right_h.home()

def background_control():
    global bg_change_count, score
    temp = game.get_background()
    for i in range(16):
        temp[i] <<= 1
        temp[i] &= 0xff
    temp[5] = 0xff
    temp[10] = 0xff
    if bg_change_count % 3 == 0:
        score += 1
        a = random.randint(6, 7)
        b = random.randint(8, 9)
        temp[a] |= 0x01
        temp[b] |= 0x01
    else:
        pass
    game.set_background(temp)
    bg_change_count += 1
def game_deinit():
    global speed, score, move_lock_flag
    score = 0
    game.set_background(b_s)

def on_button_callback3():
    global speed, score, move_lock_flag
    count = 1
    score = 0
    game.game_start()
    while True:
        speed_control()
        move_control()
        if speed != 0:
            if count % speed == 0:
                background_control()
        else:
            background_control()
        if game.background_collision_check(right_h) or game.background_collision_check(left_h):
            game.game_over()
            codey.say("wrong")
            codey.show(score)
            codey.color("#ff0000", 1)
            game_deinit()
            break

        count += 1
        time.sleep(0.05)

codey.on_button('C', on_button_callback3)

