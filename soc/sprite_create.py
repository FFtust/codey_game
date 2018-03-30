import codey 
from codey_global_board import *
import _thread
import time
from codey_ledmatrix_board import codey_ledmatrix
import math

FACE_LINE = 8
FACE_CROSS = 16
REFRESH_FREQUENCY = 50 
SPRITE_NUM_MAX = 20

NOT_MEET = 0
UP_MEET = 1
DOWN_MEET = 2
LEFT_MEET = 3
RIGHT_MEET = 4

# this is for the mismatching axis definition
def face_info_invert(dat):
    tempdata = 0
    tempdata += (dat & 0x80) >> 7
    tempdata += (dat & 0x40) >> 5
    tempdata += (dat & 0x20) >> 3
    tempdata += (dat & 0x10) >> 1
    tempdata += (dat & 0x08) << 1
    tempdata += (dat & 0x04) << 3
    tempdata += (dat & 0x02) << 5
    tempdata += (dat & 0x01) << 7
    return tempdata

# calculate the next coordinate after rotate
# angle must be multiple of 90
def calculate_coordinate_after_rotate(rotate_center, pre_coor, angle):
    # print("cal in", rotate_center, pre_coor, angle)
    pre_coor[0] = pre_coor[0] - rotate_center[0]
    pre_coor[1] = pre_coor[1] - rotate_center[1]
    angle = (angle + 360) % 360
    a_coor = [0, 0]
    a_coor[0] = round(math.cos(angle)) * pre_coor[0] + round(math.sin(angle)) * pre_coor[1]
    a_coor[1] = -1 * round(math.sin(angle)) * pre_coor[0] + round(math.cos(angle)) * pre_coor[1]
    a_coor[0] = a_coor[0] + rotate_center[0]
    a_coor[1] = a_coor[1] + rotate_center[1]
    # print("cal out", rotate_center, a_coor)
    return a_coor

def script_string_to_list(script):
    sprite_info = []
    for i in range(FACE_CROSS):
        dat = int(script[i * 2 :  (i + 1) * 2], 16)
        sprite_info.append(dat)
    return sprite_info

class sprite_create():
    def __init__(self, sp_info):
        count = 0
        p_x_l = 0
        p_x_r = 0
        p_y_u = 0
        p_y_d = 0
        self.sprite_info = []
        self.sprite_current = [0] * 16

        for i in range(FACE_CROSS):
            dat = int(sp_info[i * 2 :  (i + 1) * 2], 16)
            self.sprite_info.append(dat)
            if count == 0 and dat != 0:
                p_x_l = i
                count += 1
            elif count == 1 and dat == 0:
                p_x_r = i - 1
                count += 1
        if count == 1:
            p_x_r = 15 
 
        count = 0
        ret = 0
        print("sprite_info", self.sprite_info)
        # check the lfet_up point
        for i in range(FACE_LINE):
            for j in range(FACE_CROSS):
                ret |= self.sprite_info[j] & (1 << i)
            if count == 0 and ret != 0:
                p_y_u = i
                count += 1
            elif count == 1 and ret == 0:
                p_y_d = i - 1
                count += 1
                break
            if count > 2:
                break
            ret = 0    

        if count == 1:
            p_y_d = 7 
        self.lu_coord = [p_x_l, p_y_u]
        self.rd_coord = [p_x_r, p_y_d]
        self.rotate_angle = 0
        self.position = [0, 0]
        self.show_flag = True
        self.meet_border_status = 0 # 0: not meet 1: up 2: down 3: left 4: right
# calculate rotate center and region *******************************************************************
        self.rotate_center = [0, 0]
        self.region_len = 0 

        for i in range(2):
            self.rotate_center[i] = self.rd_coord[i] - self.lu_coord[i] + 1
            if self.rotate_center[i] % 2 == 0:
                self.rotate_center[i] = (self.rd_coord[i] + self.lu_coord[i] + 1) // 2
            else:
                self.rotate_center[i] = (self.rd_coord[i] + self.lu_coord[i]) // 2


        if (self.rd_coord[0] - self.lu_coord[0]) == (self.rd_coord[1] - self.lu_coord[1]):
            self.region_len = (self.rd_coord[0] - self.lu_coord[0]) + 1
        else:
            self.region_len = max((self.rd_coord[0] - self.lu_coord[0]), (self.rd_coord[1] - self.lu_coord[1])) + 1
            if self.region_len % 2 == 0:
                self.region_len += 1


    def add_point(self):
        pass

    def del_point(self):
        pass 

# sprite control
    def left(self, num = 1):
        self.position = [num_range_check(self.position[0] - num, -31, 31), self.position[1]]

    def right(self, num = 1):
        self.position = [num_range_check(self.position[0] + num, -31, 31), self.position[1]]

    def down(self, num = 1):
        self.position = [self.position[0], num_range_check(self.position[1] - num, -31, 31)]

    def up(self, num = 1):
        self.position = [self.position[0], num_range_check(self.position[1] + num, -31, 31)]

    def home(self):
        self.position = [0, 0]
    
    # rotate clockwisely 
    def rotate(self, angle):
        if angle % 90 == 0:
            self.rotate_angle += angle

    def rotate_to(self, angle):
        if angle % 90 == 0:
            self.rotate_angle = angle

    def show(self):
        self.show_flag = True

    def hide(self):
        self.show_flag = False

    def get_region(self):
        peak_coor = [[0, 0], [0, 0], [0, 0], [0, 0]]
        peak_coor[0] = self.lu_coord.copy()
        peak_coor[1][0] = self.rd_coord[0]
        peak_coor[1][1] = self.lu_coord[1]
        peak_coor[2] = self.rd_coord.copy()
        peak_coor[3][0] = self.lu_coord[0]
        peak_coor[3][1] = self.rd_coord[1]
        if (self.rotate_angle + 360) % 360 == 0:
            return self.lu_coord.copy(), self.rd_coord.copy()
        else:
            time_num = ((self.rotate_angle + 360) % 360) // 90
        #print("time num is", time_num)
        #print(peak_coor)
        lu = calculate_coordinate_after_rotate(self.rotate_center, peak_coor[4 - time_num], self.rotate_angle)
        rd = calculate_coordinate_after_rotate(self.rotate_center, peak_coor[2 - time_num], self.rotate_angle)
        return lu.copy(), rd.copy()

    def meet_border_check(self):
        # calculate the matrix after motion and rotation
        lu_c = [0, 0]
        rd_c = [0, 0]
        lu_c, rd_c = self.get_region()

        if self.position[0] + lu_c[0] < 0:
            self.meet_border_status = LEFT_MEET
        elif self.position[0] + rd_c[0] > 15:
            self.meet_border_status = RIGHT_MEET
        elif self.position[1] + lu_c[1] < 0:
            self.meet_border_status = UP_MEET
        elif self.position[1] + rd_c[1] > 7:
            self.meet_border_status = DOWN_MEET
        else:
            self.meet_border_status = NOT_MEET

        # print("meet_border_status", self.meet_border_status)
        # print("position", self.position)
        # print("coor", self.lu_coord, self.rd_coord)
        # print("coor after rotate", lu_c, rd_c)
        return self.meet_border_status
        

# function below shou not be called by users            
    def face_rotate_info(self):
        sr_line_num = 0
        sr_cross_num = 0
        ret_info = [0] * 16
# calculate buffer after rotate ************************************************************************* 
        sr_line_num = self.rotate_center[1] - (self.region_len) // 2
        sr_cross_num = self.rotate_center[0] - (self.region_len) // 2
        # print("start line id is:", sr_line_num, "start column id is", sr_cross_num)

        while self.rotate_angle < 0:
            self.rotate_angle += 360

        if self.rotate_angle % 360 == 90:
            temp = 0
            for i in  range(self.region_len): # column
                for j in range(self.region_len): # line
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + self.region_len - i - 1] = temp
                temp = 0

        elif self.rotate_angle % 360 == 180:
            for i in  range(self.region_len): 
                for j in range(self.region_len):
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        ret_info[sr_cross_num + self.region_len - j - 1] |= 1 << (sr_line_num + self.region_len - i - 1)

        elif self.rotate_angle % 360 == 270:
            temp = 0
            for i in  range(self.region_len):
                for j in range(self.region_len):
                    if (self.sprite_info[sr_cross_num + self.region_len - j - 1] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + i] = temp
                temp = 0
        else:
            ret_info = self.sprite_info.copy()

        self.sprite_current = [0] * 16
        for i in range(16):
            if (i + self.position[0]) >= 0 and  (i + self.position[0]) <= 15:
                if self.position[1] > 0:
                    self.sprite_current[i + self.position[0]] = (ret_info[i] >> self.position[1])
                else:
                    self.sprite_current[i + self.position[0]] = (ret_info[i] << (-self.position[1]))

        #print(self.sprite_current)

class game_base():
    def __init__(self):
        self.status = 0
        self.face_buffer = [0] * FACE_CROSS
        self.back_ground = [0] * FACE_CROSS
        self.back_ground_show = True
        self.sprite_list = []

    def set_background(self, background):
        s_list = script_string_to_list(background)
        if type(s_list) == list:
            if len(s_list) == FACE_CROSS:
                self.back_ground = s_list.copy()

    def show_background(self):
        self.back_ground_show = True

    def hide_background(self):
        self.back_ground_show = False


    def del_sprite(self, sp):
        for i in range(len(self.sprite_list)):
            if self.sprite_list[i] == sp:
                del self.sprite_list[i]

    def sprite_list_clean(self):
        self.sprite_list = []
        
    def add_sprite(self, sp):
        self.sprite_list.append(sp)

    def collision_check(self, script_1, script_2):
        start_num = script_1.lu_coord[0] + script_1.position[0]
        #print("start_num", start_num)
        for i in range(script_1.rd_coord[0] - script_1.lu_coord[0] + 1):
            if i + start_num < 0 or i + start_num > 15:
                continue
            if script_1.sprite_current[i + start_num] ^ script_2.sprite_current[i + start_num] \
             != script_1.sprite_current[i + start_num] | script_2.sprite_current[i + start_num]:
                return True
        return False

    def screen_refresh(self):
        self.face_buffer = [0] * FACE_CROSS
        for i in range(FACE_CROSS):
            for item in self.sprite_list:
                if i == 0:
                    item.face_rotate_info()
                if item.show_flag == False:
                    continue
                self.face_buffer[i] |= item.sprite_current[i]
            if self.back_ground_show:
                self.face_buffer[i] |= self.back_ground[i]
            self.face_buffer[i] = face_info_invert(self.face_buffer[i])
        codey_ledmatrix().faceplate_show(0, 0, *self.face_buffer)

    def screen_refresh_auto(self):
        while True:
            self.screen_refresh()
            time.sleep(REFRESH_FREQUENCY / 1000)

    def game_start(self):
        _thread.start_new_thread(self.screen_refresh_auto, ())


# example
# these codes is necessary 
game = game_base()
game.game_start()
# you can add a sprite like this:
## a = sprite_create("00183000000000000000000000000000")
## game.add_sprite(a)
a = sprite_create("00000010101010000000000000000000") #sprite_create("00183000000000000000000000000000")
b = sprite_create("00000010101010000000000000000000")
c = sprite_create("00000000003808000000000000000000")
d = sprite_create("00000000000000000000000000303000")
background = "01010101010101010101010101010101"
game.add_sprite(a)
game.add_sprite(b)
game.set_background(background)
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

while True:
    if codey.is_button("A"):
        a.left()
        a.meet_border_check()
    elif codey.is_button("B"):
        a.right()
        a.meet_border_check()
    elif codey.is_button("C"):
        a.rotate(90)
        a.meet_border_check()
    #if codey.dail() > 80:
    #    a.up()
    #    a.meet_border_check()
    #elif codey.dail() < 20:
    #    a.down()   
    if game.collision_check(a, b):
        print("a b collide")
    #a.rotate(90)
    #b.rotate(90)
    #c.rotate(90)
    #d.rotate(90)
    time.sleep(0.3) 