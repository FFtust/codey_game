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
game_status = GAME_WAIT_TO_PALY
barrier_list = [] 
for i in range(BARRIER_MAX_NUM):
    barrier_list.append([False, 0 , 0] ) # status, p_x, p_y

def barrier_create():
    global barrier_list
    p_x = random.randint(0, FACE_CROSS)
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] != True:
            barrier_list[i][0] = True
            barrier_list[i][1] = p_x
            barrier_list[i][2] = 0
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
    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            if barrier_list[i][1] >= plane_cur_pos and barrier_list[i][1] <= (plane_cur_pos + 2):
                if barrier_list[i][1] == plane_cur_pos + 1:
                    if barrier_list[i][2] >= 6:
                        game_status = GAME_OVER
                        codey.color("#00ff00", 1)
                else:
                    if barrier_list[i][2] == 7:
                        game_status = GAME_OVER
                        codey.color("#ff0000", 1)


def shoot():
    global plane_cur_pos
    global plane_last_pos
    global barrier_list 
    pos = 5
    codey.pixel(plane_cur_pos + 1, pos)
    codey.pixel(plane_cur_pos + 1, pos - 1)
    codey.pixel(plane_cur_pos + 1, pos - 2)
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos)
    codey.pixel(plane_cur_pos + 1, pos - 3)
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos - 1)
    codey.pixel(plane_cur_pos + 1, pos - 4) 
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos - 2)
    codey.pixel(plane_cur_pos + 1, pos - 5)
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos - 3)
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos - 4)
    time.sleep(0.01)
    codey.pixel_off(plane_cur_pos + 1, pos - 5)
    time.sleep(0.01)


    for i in range(BARRIER_MAX_NUM):
        if barrier_list[i][0] == True:
            if barrier_list[i][1] == plane_cur_pos + 1:
                barrier_list[i][0] = False
                codey.pixel_off(barrier_list[i][1], barrier_list[i][2])
        else:
            codey.pixel_off(barrier_list[i][1], barrier_list[i][2])

def barrier_control():
    barrier_create()
    face_update()
    game_over_check()
    barrier_run()



t_count = 0
def plane_contril():
    global plane_cur_pos
    global plane_last_pos 
    global t_count
    while True:
        plane_run(plane_cur_pos, plane_last_pos)
        plane_last_pos = plane_cur_pos
        if t_count % 2 == 0:
            if codey.is_button("B"):
                plane_cur_pos += 1
                if plane_cur_pos > 13:
                    plane_cur_pos = 13
            elif codey.is_button("A"):
                plane_cur_pos -= 1
                if plane_cur_pos < 0:
                    plane_cur_pos = 0
        if codey.is_button("C"):
                shoot()

        if t_count >= 10:
            barrier_control()
            t_count = 0
        t_count += 1
        time.sleep(0.020)



plane_contril() 