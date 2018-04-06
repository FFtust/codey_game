from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

score = 0
game = game_base()
game.game_start()
game_scripts = []

a_s = '10101010000000000000000000000000'
b_s = '10380000000000000000000000000000'
c_s = '30300000000000000000000000000000'
d_s = '10302000000000000000000000000000'
e_s = '30101000000000000000000000000000'

a = sprite_create(a_s)
a.hide()
b = sprite_create(b_s)
b.hide()
c = sprite_create(c_s)
c.hide()
d = sprite_create(d_s)
d.hide()
e = sprite_create(e_s)
e.hide()
game.add_sprite(a)
game.add_sprite(b)
game.add_sprite(c)
game.add_sprite(d)
game.add_sprite(e)

def line_remove_process():
    global score
    screen = game.get_screen()
    i = 0
    while i < 16:
        if screen[i] & 0xff == 0xff:
            score += 1
            del game.back_ground[i]
            game.back_ground.insert(0, 0x00)
            codey.say("start")
        i += 1
    time.sleep(0.2)

current_script = a
down_speed = 10
codey.set_variable('cmd', 0)
def on_button_callback2():
    global down_speed
    while True:
        if codey.get_variable('cmd') == 1:
            current_script.up()
            codey.set_variable('cmd', 0)          
        elif codey.get_variable('cmd') == 2:
            current_script.down()
            codey.set_variable('cmd', 0)
        elif codey.get_variable('cmd') == 3:
            current_script.rotate()
            codey.set_variable('cmd', 0)
        elif codey.get_variable('cmd') == 4:
            down_speed = 2
            codey.set_variable('cmd', 0)
        time.sleep(0.05)
         
codey.on_button('C', on_button_callback2)

def on_button_callback3():
    global current_script, down_speed, score
    while True:
        a.home()
        b.home()
        c.home()
        d.home()
        e.home()
        count = 1
        current_script = a
        others_scripts = [b, d, d, e]
        for i in range(5): 
            if i == 0:
                current_script = a
                others_scripts = [b, d, d, e]          
            if i == 1:
                current_script = b
                others_scripts = [a, c, d, e]            
            elif i == 2:
                current_script = c
                others_scripts = [a, b, d, e]  
            elif i == 3:
                current_script = d
                others_scripts = [a, b, c, e]  
            elif i == 4:
                current_script = e
                others_scripts = [a, b, c, d]

            count = 1
            down_speed = 10
            current_script.show()
            while True:
                if count % down_speed == 0:
                    current_script.right()
                
                if game.background_collision_check(current_script):
                    current_script.left()
                    codey.say("score")
                    break

                if current_script.meet_border_check() == RIGHT_MEET:
                    current_script.left()
                    codey.say("score")
                    break
     
                time.sleep(0.025)
                count += 1
            time.sleep(0.1)
            game.set_background(game.get_screen())
            a.hide()
            b.hide()
            c.hide()
            d.hide()
            e.hide()
            time.sleep(0.1)
            line_remove_process()

codey.on_button('C', on_button_callback3)

