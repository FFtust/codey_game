from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

game = game_base()
game.game_start()

a_s = '10101010000000000000000000000000'
b_s = '10380000000000000000000000000000'
c_s = '30300000000000000000000000000000'
d_s = '10180800000000000000000000000000'
e_s = '30101000000000000000000000000000'
f_s = '08181000000000000000000000000000'

current_sprite = sprite_create(b_s)
game.add_sprite(current_sprite)
def on_button_callback1():
    while True:
        if codey.is_button('A'):
            current_sprite.left()
            while codey.is_button('A'):
                time.sleep(0.1)
        elif codey.is_button('B'):
            current_sprite.right()
            while codey.is_button('B'):
                time.sleep(0.1)
        elif codey.is_button('C'):
            current_sprite.rotate()
            while codey.is_button('C'):
                time.sleep(0.1)
        time.sleep(0.05)

codey.on_button('A', on_button_callback1)

def on_button_callback3():
    while True:
        print("coord", current_sprite.lu_coord, current_sprite.rd_coord)
        print("angle",current_sprite.rotate_angle)
        print("center", current_sprite.rotate_center)
        print("xxx", current_sprite.get_region())
        print(current_sprite.meet_border_check())
        time.sleep(0.2)

codey.on_button('C', on_button_callback3)