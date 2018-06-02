from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

score = 0
game = game_base()
p_s = "80000000000000000000000000000000"
bg_s = "00000000000000000000000000000000"
p = sprite_create(p_s)
game.add_sprite(p)

game.game_start()
game.set_background(bg_s)

def move_control():
    if codey.get_variable('cmd') == 1:
        p.up()
        codey.set_variable('cmd', 0)
    elif codey.get_variable('cmd') == 2:
        p.down()
        codey.set_variable('cmd', 0)
    elif codey.get_variable('cmd') == 3:
        p.left()
        codey.set_variable('cmd', 0)
    elif codey.get_variable('cmd') == 4:
        p.right()
        codey.set_variable('cmd', 0)


down_flag = False
def test():
    global down_flag
    cont = 0
    while True:
        if cont % 2 == 0:
            p.show()
        else:
            p.hide()

        move_control()

        if codey.is_button('B'):
            p.right()
        elif codey.is_button('A'):
            p.left()
        if codey.is_button('C'):
            temp = p.get_position()
            game.set_background_with_point(temp)
        time.sleep(0.05)
        cont += 1
codey.on_start(test)

screen_list = []

def on_shake_callback():
    global screen_list
    if len(screen_list) >= 10:
        codey.say("codey")
        p.hide()
        for i in range(10):
            game.set_background(screen_list[i])
            time.sleep(0.5)
        p.show()
        screen_list = []
    else:
        codey.say("hi")
        screen_list.append(game.get_screen())
    time.sleep(0.5)

codey.on_shake(on_shake_callback)
