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
        print("face string is:", sp_info)
        for i in range(FACE_CROSS):
            dat = int(sp_info[i * 2 :  (i + 1) * 2], 16)
            print(dat)
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
        print("left_up:", self.lu_coord, "right_down:", self.rd_coord)
        self.rotate_angle = 0
        self.position = [0, 0]
    def add_point(self):
        pass

    def del_point(self):
        pass 

# srpite control
    def left(self, num = 1):
        self.position = [self.position[0] - num, self.position[1]]
        '''
        p_c = self.lu_coord[0] - num
        if p_c < 0:
            P_ = 0
        self.lu_coord = [p_c, self.lu_coord[1]]
        p_c = self.rd_coord[0] - num
        if p_c < 0:
            p_c = 0        
        self.rd_coord = [p_c, self.rd_coord[1]]
        '''

    def right(self, num = 1):
        self.position = [self.position[0] + num, self.position[1]]
        '''
        p_c = self.lu_coord[0] + num
        if p_c > FACE_CROSS:
            P_ = FACE_CROSS
        self.lu_coord = [p_c, self.lu_coord[1]]
        p_c = self.rd_coord[0] + num
        if p_c < 0:
            p_c = FACE_CROSS        
        self.rd_coord = [p_c, self.rd_coord[1]]
        '''
    def up(self, num = 1):
        self.position = [self.position[0], self.position[1] - num]

    def down(self, num = 1):
        self.position = [self.position[0], self.position[1] + num]

    def home(self):
        self.position = [0, 0]

    def rotate(self, angle):
        pass

    def rotate_to(self, angle):
        pass

    def show(self):
        pass

    def hide(self):
        pass

    def delete(self):
        del self.sprite

class game_base():
    def __init__(self):
        self.status = 0
        self.face_buffer = [0] * FACE_CROSS

        self.sprite_list = []

    def del_all_sprite(self, sp):
        pass

    def del_sprite(self):
        pass

    def sprite_list_clean(self):
        self.sprite_list = []
        
    def add_sprite(self, sp):
        self.sprite_list.append(sp)

    def screen_refresh(self):
        self.face_buffer = [0] * FACE_CROSS
        for i in range(FACE_CROSS):
            for item in self.sprite_list:
                if i + item.position[0] < 0 or  i + item.position[0] >= FACE_CROSS:
                    continue
                if item.position[1] > 0:
                    self.face_buffer[i + item.position[0]] |= (item.sprite_info[i] >> item.position[1])
                else:
                    self.face_buffer[i + item.position[0]] |= (item.sprite_info[i] << (-item.position[1]))

        codey_ledmatrix().faceplate_show(0, 0, *self.face_buffer)

    def game_start(self):
        pass


game = game_base()
a = sprite_create("00000000000003040300000000000000")
b = sprite_create("80808080808080808080808080808080")
game.add_sprite(a)
game.add_sprite(b)
game.screen_refresh()
time.sleep(1)
a.right()
b.down()
game.screen_refresh()

while True:
    if codey.is_button("A"):
        a.left()
    elif codey.is_button("B"):
        a.right()
    elif codey.is_button("C"):
        a.down()     
    if codey.dail() > 50:
        a.up()   
    game.screen_refresh()
    time.sleep(1) 