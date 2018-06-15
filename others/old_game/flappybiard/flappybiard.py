import codey
import time
import random
import rocky
import math

GAME_READY = 0
GAME_PLAYING = 1
GAME_OVER = 2
GAME_PASS = 3
START_FACE = '00000000000000000000000000000000'

BARRIER_WIDTH = 3
SPACELWIDTH = 3

game_status = GAME_READY
user_score = 0
run_speed = 40
background_face = START_FACE
add_space_flag = 0
last_column_data = '00'

axis_y = 3
count = 0
down_lock = False
music_lock = False

def game_init():
    global run_speed
    global background_face
    global add_space_flag
    global last_column_data
    global user_score
    global axis_y
    global count
    global down_lock
    global music_lock

    run_speed = 40
    background_face = START_FACE
    add_space_flag = 0
    last_column_data = '00'
    user_score = 0
    axis_y = 3
    count = 0
    down_lock = False
    music_lock = False
    codey.color("#000000")

def speed_control():
    global run_speed
    run_speed = 20 + int(codey.dail())

def create_background():
    global background_face
    global add_space_flag
    global last_column_data
    global user_score
    if add_space_flag < 3:
        background_face = background_face[2:32] + '00'
        add_space_flag += 1
    elif add_space_flag == SPACELWIDTH:
        up = random.randint(1, 3)
        down = random.randint(1, 4 - up)
        val = 255 - (int(math.pow(2, 8 - down)) - int(math.pow(2, up)))
        last_column_data = hex(val)[2:4]
        background_face = background_face[2:32] + hex(val)[2:4]
        add_space_flag += 1
    else:
        background_face = background_face[2:32] + last_column_data
        add_space_flag += 1
        if add_space_flag >= SPACELWIDTH + BARRIER_WIDTH:
            add_space_flag = 0
    user_score += 1
    return background_face

def game_over_check():
    global game_status
    global axis_y
    global background_face
    #print('the string is', background_face[14 : 16], 'y is ', axis_y)
    
    if axis_y <= 0:
        codey.color("#ff0000")
        game_status = GAME_OVER
        return

    if int(background_face[14 : 16], 16) & (1 << (7 - axis_y)) :
        print('a is', int(background_face[14 : 16], 16), 'y is', axis_y)
        codey.color("#ff0000")
        game_status = GAME_OVER

def on_start_callback():
    global game_status
    global axis_y
    global count 
    global run_speed
    global down_lock
    global music_lock
    global user_score
    last_axis_y  = 3

    codey.face("0010c7c7c7000000e3e3e3000000c3c3")
    while True:
        speed_control()
        if game_status == GAME_READY:
            if codey.is_button("C"):
                game_status = GAME_PLAYING

        elif game_status == GAME_PLAYING:
            if count % run_speed == 0:
                codey.face(create_background())
        elif game_status == GAME_OVER:
            codey.show(user_score)
            game_status = GAME_READY
            game_init()
        elif game_status == GAME_PASS:
            game_status = GAME_PLAYING

        if count % 4 == 0:
            if codey.is_button('A'):
                music_lock = False
                axis_y -= 1
                down_lock = True
            else:
                down_lock = False
                if music_lock == False:
                    codey.say('jump.wav', False, None)
                    music_lock = True

        if game_status == GAME_PLAYING:
            if count % run_speed == 0  and (not down_lock):
                axis_y += 1

            if last_axis_y != axis_y:
                codey.pixel_off(7, last_axis_y)
                codey.pixel(7, axis_y)
            last_axis_y = axis_y
            

        if axis_y >= 7:
            axis_y = 7
        elif axis_y < 0:
            axis_y = 0
        game_over_check()
        time.sleep(0.01)
        count += 1
codey.on_start(on_start_callback)
