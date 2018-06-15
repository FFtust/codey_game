from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

DIR_NONE = 0
DIR_LEFT = 1
DIR_RIGHT = 2

score = 0
game = game_base()
a_s = '00000000000000181800000000000000'
b_s = '00000000000000180800000000000000'
c_s = '00000000000000080800000000000000'
d_s = '00000000000000080000000000000000'
e_s = '30101000000000000000000000000000'
f_s = '08181000000000000000000000000000'
sprite_num = 4
sprites = [a_s, b_s, c_s, d_s]
current_script = None
move_lock_flag = False
direction = DIR_NONE

def line_remove_process():
    global score, direction
    screen = game.get_screen()
    background = game.get_background()
    removed_flag = False
    i = 0
    while i < 16:
        if screen[i] & 0xff == 0xff:
            score += 1
            removed_flag = True
            del background[i]
            if i >= 9:
                background.insert(7, 0x00)
            else:
                background.insert(6, 0x00)
        i += 1
    if removed_flag:
        codey.say("start")
    game.set_background(background)

speed = 10
codey.set_variable('cmd', 0)
def speed_control():
    global speed
    speed = codey.dail() // 5

def move_control():
    global speed, current_script, move_lock_flag, direction
    if current_script == None :
        time.sleep(0.2)
        direction = DIR_NONE
        return False
    if codey.is_button('A') and move_lock_flag == False:
        #codey.say("score")
        while not(game.background_collision_check(current_script) or current_script.meet_border_check() == LEFT_MEET):
            current_script.left()
        current_script.right()
        while codey.is_button('A'):
            pass
        return True
    elif codey.is_button('B') and move_lock_flag == False:
        #codey.say("score")
        while not(game.background_collision_check(current_script) or current_script.meet_border_check() == RIGHT_MEET):
            current_script.right()
        current_script.left()
        while codey.is_button('B'):
            pass
        return True
    elif codey.is_button('C') and move_lock_flag == False:
        current_script.rotate()
        while codey.is_button('C'):
            pass
        if game.background_collision_check(current_script):
            return True
    return False

def background_control():
    background = game.get_background()
    temp1 = 0
    for i in range(7):
        temp1 |= ((background[i] & 0x01) << i)
    temp2 = 0
    for i in range(7):
        temp2 |= ((background[9 + i] & 0x80) >> (7 - i))

    for i in range(7):
        background[i] = (background[i] >> 1) & 0xff
        if (temp2 & (1 << (6 - i))):
            background[i] |= 0x80
        background[i + 9] = (background[i + 9] << 1) & 0xff
        if (temp1 & (1 << (6 - i))):
            background[i + 9] |= 0x01
    game.set_background(background)

def on_button_callback3():
    global current_script, speed, score, move_lock_flag
    game.game_start()
    game.set_background([4,4,4,0,0,0,0,0,0,0,0,0,0,1,1,1])
    while True:
        index = random.randint(0, sprite_num - 1)
        current_script = sprite_create(sprites[index])
        game.add_sprite(current_script)
        if game.background_collision_check(current_script):
             game.del_sprite(current_script)
             current_script = None
             codey.say("wrong")
             game.game_over()
             codey.show(score)
             score = 0
             break
        count = 1
        speed = 10
        while True:
            if count % speed == 0:
                 background_control()
                 line_remove_process()
            if move_control():
                break
            speed_control()
            time.sleep(0.05)
            count += 1
        time.sleep(0.1)
        game.set_background(game.get_screen())
        current_script.hide()
        time.sleep(0.1)
        game.del_sprite(current_script)
        move_lock_flag = False

codey.on_button('C', on_button_callback3)

