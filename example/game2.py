from game import game_base
from game import sprite_create
import codey 
import time
import random

step_str = "80808000000000000000000000000000"
game = game_base()
game.game_start()
a = sprite_create(step_str)
b = sprite_create(step_str)
c = sprite_create(step_str)
d = sprite_create(step_str)
person = sprite_create("00004000000000000000000000000000")
game.add_sprite(person)
game.add_sprite(a)
game.add_sprite(b)
b.right(2)
b.up(2)
game.add_sprite(c)
c.right(3)
c.up(4)
game.add_sprite(d)
d.right(4)
d.up(6)

def on_button_callback():
    count = 0
    sign = [1, 1, 1, 1]
    while True:
        if count % 2 == 0:
            d.right(1 * sign[3])
        if count % 3 == 0:
            c.right(1 * sign[2])
        if count % 4 == 0:
            b.right(1 * sign[1])
        if count % 5 == 0:
            a.right(1 * sign[0])

        if a.meet_border_check() == 3:
            print("a left")
            sign[0] = 1
        elif a.meet_border_check() == 4:
            print("a right")
            sign[0] = -1
        if b.meet_border_check() == 3:
            sign[1] = 1
        elif b.meet_border_check() == 4:
            sign[1] = -1
        if c.meet_border_check() == 3:
            sign[2] = 1
        elif c.meet_border_check() == 4:
            sign[2] = -1
        if d.meet_border_check() == 3:
            sign[3] = 1
        elif d.meet_border_check() == 4:
            sign[3] = -1

        count += 1
        time.sleep(0.1)

codey.on_button('A', on_button_callback)

def on_button_callback1():
    person.up(1)
    time.sleep(0.05)
    person.up(1)
    time.sleep(0.2)
    person.down(1)
    while True:
        if game.collision_check(person, a):
            break
        elif game.collision_check(person, b):
            break
        elif game.collision_check(person, c):
            break
        elif game.collision_check(person, d):
            break 
        if person.d.meet_border_check() == 2:
            codey.show("game over")
            break
        person.down(1)
        time.sleep(0.2)
    print("out")
codey.on_button('C', on_button_callback1)