import codey 
import _thread
import time
from codey_ledmatrix_board import codey_ledmatrix

FACE_LINE = 8
FACE_CROSS = 16
REFRESH_FREQUENCY = 50 
SPRITE_NUM_MAX = 20

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
            self.sprite_info.append(codey.face_info_invert(dat))
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

# srpite control
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

    def face_rotate_info(self):
        sr_line_num = 0
        sp_line_num = 0
        sr_cross_num = 0
        sp_cross_num = 0
        ret_info = [0] * 16
        region_len = max((self.rd_coord[0] - self.lu_coord[0]), (self.rd_coord[1] - self.lu_coord[1]))
        print("region is", self.lu_coord, self.rd_coord)
        sr_line_num = self.lu_coord[1]
        sp_line_num = sr_line_num + region_len
        sr_cross_num = self.lu_coord[0]
        sp_cross_num = sr_cross_num + region_len

        if self.rotate_angle < 0:
            self.rotate_angle += 360
        if self.rotate_angle % 360 == 90:
            print(self.sprite_info)
            temp = 0
            #print("region len is", region_len)
            for j in  range(region_len + 1):
                for i in range(region_len + 1):
                    if (self.sprite_info[sr_cross_num + i] & (1 << (sr_line_num + j))):
                        temp |=  (1 << (i + region_len))
                print(temp)
                ret_info[sr_cross_num + region_len - j] = temp
                temp = 0

            #print("ret info is", ret_info)
            return ret_info
        elif self.rotate_angle % 360 == 180:
            pass
        elif self.rotate_angle % 360 == 270:
            pass    
        else:
            return self.sprite_info 

    def show(self):
        self.show_flag = True

    def hide(self):
        self.show_flag = False


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


game = game_base()
game.game_start()

a = sprite_create("00000000000000101810000000000000")
game.add_sprite(a)
time.sleep(1)

while True:
    if codey.is_button("A"):
        a.left()
    elif codey.is_button("B"):
        a.right()
    elif codey.is_button("C"):
        a.rotate(90)
    if codey.dail() > 50:
        a.up()   
    time.sleep(0.5) 