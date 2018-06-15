import codey
import time
import random
import rocky

MOVE_NOT = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4

FACE_CROSS = 16
FACE_LINE = 8

GAME_READY = 0
GAME_PLAYING = 1
GAME_OVER = 2
GAME_PASS = 3
GAME_LEVEL_PASS = 4

LEVEL_MAX = 5
LEVEL_POINT_NUM = [10, 20, 40, 60, 100]
LEVEL_RUN_SPEED = [15, 10, 5, 2, 2]
snake_list = [[0, 0], [2, 3], [3, 3]]
game_status = GAME_READY

food_point = [0, 0]
user_score = 0
run_speed = 22
def game_over_check():
    global snake_list
    global game_status
    #print("list", snake_list)
    if snake_list[-1] in snake_list[0 : (len(snake_list) - 1)]:
        game_status = GAME_OVER
        codey.say('death.wav')
        codey.color("#ff0000", 1)

def show_snake():
    global snake_list
    for i in range(len(snake_list)):
        if i == 0:
            codey.pixel_off(snake_list[i][0], snake_list[i][1])
        else:
            codey.pixel(snake_list[i][0], snake_list[i][1])

def snake_add_point(p_x, p_y):
    snake_list.append([p_x, p_y])
    codey.say('score.wav')

food_create_order_list = [[1,2,3,4], [2,3,1,4], [4,3,1,2], [3,4,1,2], [3,4,2,1]]
def point_create():
    global food_point
    global user_score
    global game_status
    user_score += 1
    p_x = random.randint(0, 15)
    p_y = random.randint(0, 7)

    order = random.randint(0, 3)
    for item in food_create_order_list[order]:
        out_point = check_region_not_full(p_x, p_y, item)
        if out_point == None:
            if item == food_create_order_list[order][-1]:
                game_status = GAME_PASS
            else:
                continue
        else:
            food_point = out_point
            codey.pixel(food_point[0], food_point[1])

            return food_point
    food_point = [0, 0]
    codey.pixel(0, 0)
    return None

def sanke_move(dir):
    global snake_list
    global food_point

    if dir == MOVE_UP:
        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_y != 0:
            point_t = [p_x, p_y - 1]
        else:
            point_t = [p_x, 7]

        if point_t == food_point:
            snake_add_point(food_point[0], food_point[1])
            print("create result", point_create())
        # else:  
        for i in range(len(snake_list) - 1):
            snake_list[i] = snake_list[i + 1] 

        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_y != 0:
            snake_list[-1] = [p_x, p_y - 1]
        else:
            snake_list[-1] = [p_x, 7]

    elif dir == MOVE_DOWN:
        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_y != 7:
            point_t = [p_x, p_y + 1]
        else:
            point_t = [p_x, 0]

        if point_t == food_point:
            snake_add_point(food_point[0], food_point[1])
        # else:  
        for i in range(len(snake_list) - 1):
            snake_list[i] = snake_list[i + 1] 

        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_y != 7:
            snake_list[-1] = [p_x, p_y + 1]
        else:
            snake_list[-1] = [p_x, 0]


    elif dir == MOVE_LEFT:
        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_x != 0:
            point_t = [p_x - 1, p_y]
        else:
            point_t = [15, p_y]

        if point_t == food_point:
            snake_add_point(food_point[0], food_point[1])
        # else:  
        for i in range(len(snake_list) - 1):
            snake_list[i] = snake_list[i + 1] 

        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_x != 0:
            snake_list[-1] = [p_x - 1, p_y]
        else:
            snake_list[-1] = [15, p_y]

    elif dir == MOVE_RIGHT:
        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_x != 15:
            point_t = [p_x + 1, p_y]
        else:
            point_t = [0, p_y]

        if point_t == food_point:
            snake_add_point(food_point[0], food_point[1])
        # else:  
        for i in range(len(snake_list) - 1):
            snake_list[i] = snake_list[i + 1] 

        p_x = snake_list[-1][0]
        p_y = snake_list[-1][1]
        if p_x != 15:
            snake_list[-1] = [p_x + 1, p_y]
        else:
            snake_list[-1] = [0, p_y]

    if point_t == food_point:
        print("create result", point_create())
    game_over_check()

def check_region_not_full(p_x, p_y, region): # region 1: up_left 2: down_left 3: right_up 4: right_down
    global snake_list
    x = p_x
    y = p_y
    if region == 1:
        while y >= 0 and y <= 7:  
            if not ([x, y] in snake_list):
                return [x, y]
            else:
                if x >= 0:
                    x = x - 1
                else:
                    y = y -1
                    x = p_x
    elif region == 2:
        while y >= 0 and y <= 7: 
            if not ([x, y] in snake_list):
                return [x, y]
            else:
                if x >= 0:
                    x = x - 1
                else:
                    y = y + 1
                    x = p_x
    elif region == 3:
        while y >= 0 and y <= 7: 
            if not ([x, y] in snake_list):
                return [x, y]
            else:
                if x <= 15:
                    x = x + 1
                else:
                    y = y -1
                    x = p_x

    elif region == 4:
        while y >= 0 and y <= 7: 
            if not ([x, y] in snake_list):
                return [x, y]
            else:
                if x <= 15:
                    x = x + 1
                else:
                    y = y + 1
                    x = p_x
    return None

def speed_control():
    global run_speed
    global level_cur
    run_speed = LEVEL_RUN_SPEED[level_cur - 1]

def level_update():
    global level_cur
    global snake_list
    global game_status

    if len(snake_list) >= LEVEL_POINT_NUM[level_cur - 1]:
        level_cur += 1
        if level_cur >= LEVEL_MAX:
            game_status = GAME_PASS
        else:
            game_status = GAME_LEVEL_PASS

show_snake()
move_dir = MOVE_NOT
move_dir_last = MOVE_NOT
count = 0
level_cur = 1
print("create result", point_create())
while True:
    level_update()
    speed_control()
    if game_status == GAME_READY:
        if codey.is_button("C"):
            game_status = GAME_PLAYING

    elif game_status == GAME_PLAYING:
        if codey.is_tilt('forward'):
            if move_dir_last != MOVE_DOWN:
                move_dir = MOVE_UP
        elif codey.is_tilt('backward'):
            if move_dir_last != MOVE_UP:
                move_dir = MOVE_DOWN
        elif codey.is_tilt('left'):
            if move_dir_last != MOVE_RIGHT:
                move_dir = MOVE_LEFT
        elif codey.is_tilt('right'):
            if move_dir_last != MOVE_LEFT:
                move_dir = MOVE_RIGHT

        codey.pixel(food_point[0], food_point[1])

        if count % run_speed == 0:
            sanke_move(move_dir)  
            move_dir_last = move_dir
        show_snake()

        if codey.is_button("A"):
            game_status = GAME_OVER

    elif game_status == GAME_OVER:
        codey.show(len(snake_list) - 3)
        if codey.is_button("C"):
            snake_list = [[0, 0], [2, 3], [3, 3]]
            codey.clear()
            food_point = [0, 0]
            show_snake()
            print("create result", point_create())
            game_status = GAME_PLAYING

    elif game_status == GAME_PASS:
        codey.show("OK")
        if codey.is_button("C"):
            snake_list = [[0, 0], [2, 3], [3, 3]]
            codey.clear()
            food_point = [0, 0]
            print("create result", point_create())
            show_snake()
            game_status = GAME_PLAYING
    elif game_status == GAME_LEVEL_PASS:
        if str_show_flag == 1:
            codey.show("LEVEL1" + str(level_cur))
            str_show_flag = 0

        if codey.is_button("C"):
            snake_list = [[0, 0], [2, 3], [3, 3]]
            codey.clear()
            food_point = [0, 0]
            print("create result", point_create())
            show_snake()
            game_status = GAME_PLAYING
            str_show_flag = 1

    time.sleep(0.02)
    count += 1