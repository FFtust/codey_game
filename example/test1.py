import codey 
import _thread
import time
from codey_ledmatrix_board import codey_ledmatrix

FACE_LINE = 8
FACE_CROSS = 16
REFRESH_FREQUENCY = 50 
SPRITE_NUM_MAX = 20

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

class sprite_create():
    def __init__(self, sp_info):
        count = 0
        p_x_l = 0
        p_x_r = 0
        p_y_u = 0
        p_y_d = 0
        self.sprite_info = []
        for i in range(FACE_CROSS):
            dat = int(sp_info[i * 2 :  (i + 1) * 2], 16)
            self.sprite_info.append(face_info_invert(dat))
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
    def add_point(self):
        pass

    def del_point(self):
        pass 

# sprite control
    def left(self, num = 1):
        self.position = [self.position[0] - num, self.position[1]]

    def right(self, num = 1):
        self.position = [self.position[0] + num, self.position[1]]
    def up(self, num = 1):
        self.position = [self.position[0], self.position[1] - num]

    def down(self, num = 1):
        self.position = [self.position[0], self.position[1] + num]

    def home(self):
        self.position = [0, 0]

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

    def is_meet_border(self, dir):
        
        return False

        return True

# function below shou not be called by users            
    def face_rotate_info(self):
        sr_line_num = 0
        sp_line_num = 0
        sr_cross_num = 0
        sp_cross_num = 0
        ret_info = [0] * 16
        region_len = max((self.rd_coord[0] - self.lu_coord[0]), (self.rd_coord[1] - self.lu_coord[1]))
        sr_line_num = self.lu_coord[1]
        sr_cross_num = self.lu_coord[0]

        if self.rotate_angle < 0:
            self.rotate_angle += 360
        if self.rotate_angle % 360 == 90:
            temp = 0
            for i in  range(region_len + 1):
                for j in range(region_len + 1):
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + region_len - i] = temp
                temp = 0
            return ret_info
        elif self.rotate_angle % 360 == 180:
            for i in  range(region_len + 1): 
                for j in range(region_len + 1):
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        ret_info[sr_cross_num + region_len - j] |= 1 << (sr_line_num + region_len - i)
            return ret_info
        elif self.rotate_angle % 360 == 270:
            temp = 0
            for i in  range(region_len + 1):
                for j in range(region_len + 1):
                    if (self.sprite_info[sr_cross_num + region_len - j] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + i] = temp
                temp = 0

            return ret_info
        else:
            return self.sprite_info 

class game_base():
    def __init__(self):
        self.status = 0
        self.face_buffer = [0] * FACE_CROSS

        self.sprite_list = []

    def del_sprite(self, sp):
        for i in range(len(self.sprite_list)):
            if self.sprite_list[i] == sp:
                del self.sprite_list[i]

    def sprite_list_clean(self):
        self.sprite_list = []
        
    def add_sprite(self, sp):
        self.sprite_list.append(sp)

    def screen_refresh(self):
        self.face_buffer = [0] * FACE_CROSS
        for i in range(FACE_CROSS):
            for item in self.sprite_list:
                if item.show_flag == False:
                    continue
                if i + item.position[0] < 0 or  i + item.position[0] >= FACE_CROSS:
                    continue
                temp = item.face_rotate_info()
                if item.position[1] > 0:
                    self.face_buffer[i + item.position[0]] |= (temp[i] >> item.position[1])
                else:
                    self.face_buffer[i + item.position[0]] |= (temp[i] << (-item.position[1]))

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
a = sprite_create("00002020200000000000000000000000")
game.add_sprite(a)
time.sleep(1)
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
        a.up()
    elif codey.is_button("B"):
        a.down()
    elif codey.is_button("C"):
        a.rotate(90) 
    time.sleep(0.05) 