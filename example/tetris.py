from game import game_base
from game import sprite_create
import codey 
import time
import random

game = game_base()
game.game_start()
game_scripts = []

a_s = '10101010000000000000000000000000'
b_s = '10380000000000000000000000000000'
c_s = '30300000000000000000000000000000'
d_s = '10302000000000000000000000000000'
e_s = '30101000000000000000000000000000'

def 
a = sprite_create("00183000000000000000000000000000")
#background = "ff8181818181818181818181818181ff"
#game.set_background(background)
#plane = sprite_create("000000000000c020c000000000000000")
game.add_sprite(b)
game.add_sprite(a)
#background = "ff8181818181818181818181818181ff"
#game.add_sprite(a)
#game.add_sprite(b)
#game.set_background(background)
#game.add_sprite(c)
#game.add_sprite(d)
# after add the sprite, you can control the sprite like this:
## sprite.rotate(90)
## sprite.rotate_to(90)
## sprite.up()
## sprite.down()
## sprite.left()
## sprite.right()
## sprite.home()

cur_direc = 1 # 1: right-up 2: right-down 3: left-up 4: left-down
last_direc = 1
speed = 1
b.up()
def on_button_callback():
    global cur_direc, last_direc
    b.left()

codey.on_button('A', on_button_callback)

def on_button_callback1():
    global cur_direc, last_direc
    b.right()

codey.on_button('B', on_button_callback1)

def on_button_callback2():
    global cur_direc, last_direc
    count = 0
    while True:
        speed = codey.dail() // 10
        if cur_direc == 1:
            if a.meet_border_check() == 0x01: # up
                cur_direc = 2
            elif a.meet_border_check() == 0x08: # right
                cur_direc = 3
        elif cur_direc == 2:
            if a.meet_border_check() == 0x02: # down
                cur_direc = 1
            elif a.meet_border_check() == 0x08: # right
                cur_direc = 4
            elif game.collision_check(a, b):
                cur_direc = 1
                codey.say('jump.wav', False)

        elif cur_direc == 3:
            if a.meet_border_check() == 0x01: # up
                cur_direc = 4
            elif a.meet_border_check() == 0x04: # left
                cur_direc = 1     
        elif cur_direc == 4:
            if a.meet_border_check() == 0x02: # down
                cur_direc = 3
            elif a.meet_border_check() == 0x04: # left
                cur_direc = 2
            elif game.collision_check(a, b):
                cur_direc = 3
                codey.say('jump.wav', False)

        if cur_direc == 1:
            a.up()
            a.right()
        elif cur_direc == 2:
            a.down()
            a.right()
        elif cur_direc == 3:
            a.left()
            a.up()          
        elif cur_direc == 4:
            a.left()
            a.down()

        time.sleep(1.05 - speed / 10)
            
codey.on_button('C', on_button_callback2)
