import codey
import time
import random
import rocky

BARRIER_MAX_NUM = 10
FACE_CROSS = 16
FACE_LINE = 8
UPDATE_TIME = 0.5 # s

GAME_WAIT_TO_PALY = 0
GAME_PLAYING  = 1
GAME_OVER  = 2

plane_cur_pos = 6
plane_last_pos = 7
barrier_list = [] 
for i in range(BARRIER_MAX_NUM):
    barrier_list.append([False, 0 , 0] ) # status, p_x, p_y

user_score = 0

def barrier_create():
    global barrier_list
    global user_score
    p_x = random.randint(0, FACE_CROSS)
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] != True:
            barrier_list[i][0] = True
            barrier_list[i][1] = p_x
            barrier_list[i][2] = 0
            user_score += 1
            break

def barrier_run():
    global barrier_list
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            barrier_list[i][2] += 1

def plane_run(p_x_c, p_x_l):
    if p_x_c != p_x_l:
        codey.pixel_off(p_x_l, 7)
        codey.pixel_off(p_x_l + 1, 6)
        codey.pixel_off(p_x_l + 2, 7)

        codey.pixel(p_x_c, 7)
        codey.pixel(p_x_c + 1, 6)
        codey.pixel(p_x_c + 2, 7)    

def face_update():
    global barrier_list
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            codey.pixel_off(barrier_list[i][1], barrier_list[i][2] - 1)
            if barrier_list[i][2] >= FACE_LINE:
                barrier_list[i][0] = False
            else:
                codey.pixel(barrier_list[i][1], barrier_list[i][2])
        else:
            codey.pixel_off(barrier_list[i][1], barrier_list[i][2])

def game_over_check():
    global plane_cur_pos
    global plane_last_pos
    global barrier_list 
    global game_status
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            if barrier_list[i][1] >= plane_cur_pos and barrier_list[i][1] <= (plane_cur_pos + 2):
                if barrier_list[i][1] == plane_cur_pos + 1:
                    if barrier_list[i][2] >= 6:
                        game_status = GAME_OVER
                        codey.color("#ff0000", 1)
                else:
                    if barrier_list[i][2] == 7:
                        game_status = GAME_OVER
                        codey.color("#ff0000", 1)


def shoot():
    global plane_cur_pos
    global plane_last_pos
    global barrier_list 
    plane_c_pos = plane_cur_pos
    pos = 5
    codey.say("gunshot.wav")
    codey.pixel(plane_c_pos + 1, pos)
    codey.pixel(plane_c_pos + 1, pos - 1)
    codey.pixel(plane_c_pos + 1, pos - 2)
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos)
    codey.pixel(plane_c_pos + 1, pos - 3)
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos - 1)
    codey.pixel(plane_c_pos + 1, pos - 4) 
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos - 2)
    codey.pixel(plane_c_pos + 1, pos - 5)
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos - 3)
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos - 4)
    time.sleep(0.01)
    codey.pixel_off(plane_c_pos + 1, pos - 5)
    time.sleep(0.01)


    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            if barrier_list[i][1] == plane_c_pos + 1:
                barrier_list[i][0] = False
                codey.pixel_off(barrier_list[i][1], barrier_list[i][2])
        else:
            codey.pixel_off(barrier_list[i][1], barrier_list[i][2])

def barrier_control():
    barrier_create()
    face_update()
    game_over_check()
    barrier_run()

barrier_move_speed = 11
def barruer_speed_control():
    global barrier_move_speed
    barrier_move_speed = 11 - int(codey.dail() / 10)

t_count = 0
game_status = GAME_WAIT_TO_PALY
def plane_contril():
    global plane_cur_pos
    global plane_last_pos 
    global t_count
    global user_score
    global game_status
    global barrier_list
    global barrier_move_speed

    while True:
        barruer_speed_control()
        if game_status == GAME_WAIT_TO_PALY:
            codey.face('00000000000003e60300000000000000')
            if codey.is_button("C"):
                game_status = GAME_PLAYING
                codey.clear()
        elif game_status == GAME_OVER:
            codey.show(user_score)
            for i in range(BARRIER_MAX_NUM):
                barrier_list[i][0] =False
            if codey.is_button("C"):
                game_status = GAME_PLAYING
                plane_cur_pos = 7
                plane_last_pos = 6
                user_score = 0
                codey.clear()
        elif game_status == GAME_PLAYING: 
            plane_run(plane_cur_pos, plane_last_pos)
            plane_last_pos = plane_cur_pos
            if codey.is_button("C"):
                shoot()
            if t_count >= barrier_move_speed:
                barrier_control()
                t_count = 0
            t_count += 1
            time.sleep(0.020)

def button_a_cb():
    global plane_cur_pos
    global plane_last_pos 
    plane_cur_pos -= 1
    if plane_cur_pos < 0:
        plane_cur_pos = 0

def button_b_cb():
    global plane_cur_pos
    global plane_last_pos 
    plane_cur_pos += 1
    if plane_cur_pos > 13:
        plane_cur_pos = 13

codey.on_button("A", button_a_cb)
codey.on_button("B", button_b_cb)

def main_fun():
    plane_contril()

codey.on_start(main_fun) 