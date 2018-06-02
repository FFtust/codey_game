from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

score = 0
game = game_base()
bg_s = '81818181818181818181818181818181'
a_s = '10101010000000000000000000000000'
c_s = '00000000000000000000000000030000'
p_s = "40000000000000000000000000000000"

a = sprite_create(a_s)
b = sprite_create(a_s)
c = sprite_create(c_s)
p = sprite_create(p_s)

game.add_sprite(a)
game.add_sprite(b)
game.add_sprite(c)
game.add_sprite(p)
a.right(1)
b.right(8)
#c.hide()

game.game_start()
game.set_background(bg_s)

down_flag = False
def test():
    global down_flag
    count = 0
    while True:
        if count % 2 == 0:
            p.show()
        else:
            p.hide()

        if count % 10 == 0:
            a.rotate()
        if count % 2 == 0:
            b.rotate()
        if count % 15 == 0:
            down_flag = True
            c.show()

        if down_flag:
            c.down()
            if c.meet_border_check() == DOWN_MEET:
                c.hide()
                c.home()
                down_flag = False
        
        if codey.is_button('B'):
            p.right()
        elif codey.is_button('A'):
            p.left()

        if game.collision_check(p, a) or game.collision_check(p, b) or game.collision_check(p, c):
            codey.say("wrong")
            codey.color("#ff0000", 0.05)
            p.home()

        time.sleep(0.05)
        count += 1
codey.on_start(test)

 