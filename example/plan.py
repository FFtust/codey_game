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

plane_s = '000000000000c060c000000000000000'
plane_s1 = '000000000000c0e0c000000000000000'
plane_s2 = '00000000000080408000000000000000'

bullet_s =  "000000000000001c0000000000000000"
bullet_s1 =  "00000000000040204000000000000000"
bullet_s2 =  "00000000000000101000000000000000"

plane_id = 0
bullet_id = 0

bullet_run_count = 0
bullet_run_flag = False

plane = None
bullet = None

music_name = "shot"

def background_control():
    global score
    temp = game.get_background()
    
    if score < 50:
        a = random.randint(0, 15)
    elif score < 100:
        a = random.randint(0, 7)
        b = random.randint(8, 15)
    else:
        a = random.randint(0, 5)
        b = random.randint(6, 11)
        c = random.randint(7, 15)

    for i in range(16):
        temp[i] <<= 1
        temp[i] &= 0xff
        if score < 50:
            if i == a:
                temp[i] |= 0x01
        elif score < 100:
            if i == a or i == b:
                temp[i] |= 0x01
        else:
            if i == a or i == b or i == c:
                temp[i] |= 0x01            

    game.set_background(temp)

def barrier_delete():
    global score, bullet_id
    temp = game.get_background()
    i = bullet.get_position()[0]
    if bullet_id == 0:
        temp[i + 7] = 0x00
    elif bullet_id == 1:
        temp[i + 6] &= (1 << bullet.get_position()[1] - 1)
        temp[i + 6] &= (1 << bullet.get_position()[1])
        temp[i + 6] &= (1 << bullet.get_position()[1] + 1)
        temp[i + 7] &= (1 << bullet.get_position()[1] - 1)
        temp[i + 7] &= (1 << bullet.get_position()[1])
        temp[i + 7] &= (1 << bullet.get_position()[1] + 1)
        temp[i + 8] &= (1 << bullet.get_position()[1] - 1)
        temp[i + 8] &= (1 << bullet.get_position()[1])
        temp[i + 8] &= (1 << bullet.get_position()[1] + 1)
    elif bullet_id == 2:
        temp[i + 7] &= 1 << (bullet.get_position()[1])
    game.set_background(temp)  

def bullet_move_control():
    global bullet_run_flag, bullet_run_count, score, music_name, bullet_id
    if codey.is_button('C'):
        bullet_run_flag = True
    
    if bullet_id == 0:
        move_step = 5
    elif bullet_id == 1:
        move_step = 5
    else:
        move_step = 7

    if bullet_run_flag:
        if bullet_run_count == 0:
            codey.say(music_name)
            bullet.set_position(plane.get_position()) 
            bullet.show()
            bullet_run_count += 1
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        elif bullet_run_count < move_step:
            bullet.up()
            print(bullet.get_position())
            bullet_run_count += 1
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        else:
            bullet.home()
            bullet.hide()
            bullet_run_count = 0
            bullet_run_flag = False

def plane_move_control():
    global plane
    if plane == None:
        return
    if codey.is_button('A'):
        plane.left()
    elif codey.is_button('B'):
        plane.right()


game_status = 0
def main():
    global game_status, score, plane_id, plane, music_name, bullet, bullet_id
    count = 0

    while True:
        if game_status == 0:
            if plane_id == 0:
                codey.face(plane_s)
            elif plane_id == 1:
                codey.face(plane_s1)
            else:
                codey.face(plane_s2)

            if codey.is_button("C"):
                codey.say("start")
                game_status = 1
                score = 0
                if plane_id == 0:
                    plane = sprite_create(plane_s)
                    music_name = "shot"
                elif plane_id == 1:
                    plane = sprite_create(plane_s1)
                    music_name = "laser"
                else:
                    plane = sprite_create(plane_s2)
                    music_name = "score"

                if bullet_id == 0:
                    bullet = sprite_create(bullet_s)
                elif bullet_id == 1:
                    bullet = sprite_create(bullet_s1)
                else:
                    bullet = sprite_create(bullet_s2)

                game.add_sprite(plane)
                bullet.hide()
                game.add_sprite(bullet)

                game.game_start()
                time.sleep(1)
            elif codey.is_button("A"):
                plane_id += 1
                if plane_id > 2:
                    plane_id = 0
                while codey.is_button("A"):
                    pass
            elif codey.is_button("B"):
                bullet_id += 1
                if bullet_id > 2:
                    bullet_id = 0
                while codey.is_button("B"):
                    pass

        elif game_status == 1:
            bullet_move_control()
            if count % 2 == 0:
                plane_move_control()
            if count % (codey.dail() // 6) == 0:
                background_control()
            if game.background_collision_check(plane):
                codey.say('wrong')
                game_status = 2
                game.set_background("00000000000000000000000000000000")
                game.sprite_list_clean()
                # print(11111)
                # game.del_sprite(plane)
                # print(11222)
                # game.del_sprite(bullet)

                print(11444)
                palne = None
                bullet = None
                game.game_over()
            time.sleep(0.02)
        else:
            codey.show(score)
            if codey.is_button("C"):
                game_status = 0
            time.sleep(0.1)
        count += 1

#codey.on_start(main)
main()
