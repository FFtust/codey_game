import codey
from makeblock import ledmatrix
import time
import random
import rocky
import math

# note table
loop_times = 1

note_table = \
(
  [60, 0.25],
  [62, 0.25],
  [64, 0.25],
  [60, 0.25],
  [60, 0.25],
  [62, 0.25],
  [64, 0.25],
  [60, 0.25],
  [64, 0.25],
  [65, 0.25],
  [67, 0.5],
  [64, 0.25],
  [65, 0.25],
  [67, 0.5],
  [67, 0.375],
  [69, 0.125],
  [67, 0.375],
  [65, 0.125],
  [64, 0.25],
  [60, 0.25],
  [67, 0.375],
  [69, 0.125],
  [67, 0.375],
  [65, 0.125],
  [64, 0.25],
  [60, 0.25],
  [62, 0.25],
  [55, 0.25],
  [60, 0.5],
  [62, 0.25],
  [55, 0.25],
  [60, 0.5],
)
note_play_index = 0
single_note_show_over = True
single_note_show_row_num = 1
single_note_show_current_row_num = 1
single_bote_play_over = True
note_interval_current_row = 0
update_row_num = 0
# note table

GAME_READY = 0
GAME_PLAYING = 1
GAME_OVER = 2
GAME_PASS = 3
START_FACE = [0] * 16

NOTE_LEFT_COLUMN = 2
NOTE_MIDDLE_COLUMN = 7
NOTE_RIGHT_COLUMN = 12
NOTE_COLUMN_NUM = 3
NOTE_INTERVAL_ROW = 2

NOTE_LEFT_MAX = 63
NOTE_MIDDLE_MAX = 100
NOTE_RIGHT_MAX = 66


game_status = 0
run_speed = 20
user_score = 0

current_backgroup = START_FACE

def game_init():  
    global user_score
    global current_backgroup
    global note_play_index
    global single_note_show_over
    global single_bote_play_over
    global single_note_show_row_num
    global note_interval_current_row
    global single_note_show_current_row_num
    global update_row_num
    user_score = 0
    current_backgroup = [0] * 16
    note_play_index = 0
    single_note_show_over = True
    single_note_show_row_num = 1
    single_note_show_current_row_num = 1
    single_bote_play_over = True
    note_interval_current_row = 0
    update_row_num = 0

def speed_control():
    global run_speed
    run_speed = 20 + int(codey.dail())

def note_show_row_num_cal(note_t):
    row_num = round(note_t * 4)
    if row_num == 0:
      		row_num += 1
    #return row_num
    return 1

def update_background():
    global current_backgroup
    global note_play_index
    global single_note_show_over
    global single_bote_play_over
    global single_note_show_row_num
    global note_interval_current_row
    global single_note_show_current_row_num
    global update_row_num

    if update_row_num >= len(note_table) * 3 + 8:
        return False
    elif note_play_index < len(note_table):
        if single_note_show_over:
            single_note_show_row_num = note_show_row_num_cal(note_table[note_play_index][1])
            single_note_show_current_row_num = 1
            update_value = 0x80
            single_note_show_over = False
        else:
            if single_note_show_current_row_num >= single_note_show_row_num:
                update_value = 0
                note_interval_current_row += 1
                if note_interval_current_row >= NOTE_INTERVAL_ROW:
                    single_note_show_over = True
                    single_note_show_current_row_num = 0
                    note_play_index = note_play_index + 1
                    note_interval_current_row = 0
            else:
                single_note_show_current_row_num += 1
                update_value = 0x80
    update_row_num += 1
    for i in range(16):
        current_backgroup[i] = (current_backgroup[i] >> 1) & 0xff

    if note_play_index >= len(note_table):
        show_face = current_backgroup.copy()
        for i in range(16):
            show_face[i] = show_face[i] | 0x01   
        ledmatrix().faceplate_show(0, 0, *show_face)
        return True

    if note_table[note_play_index][0] < NOTE_LEFT_MAX:
        for i in range(NOTE_LEFT_COLUMN, NOTE_LEFT_COLUMN + NOTE_COLUMN_NUM):
            current_backgroup[i] |= update_value
    elif note_table[note_play_index][0] < NOTE_RIGHT_MAX:
        for i in range(NOTE_RIGHT_COLUMN, NOTE_RIGHT_COLUMN + NOTE_COLUMN_NUM):
            current_backgroup[i] |= update_value
    else:
        for i in range(NOTE_MIDDLE_COLUMN, NOTE_MIDDLE_COLUMN + NOTE_COLUMN_NUM):
            current_backgroup[i] |= update_value
    print(current_backgroup)
    show_face = current_backgroup.copy()
    for i in range(16):
        show_face[i] = show_face[i] | 0x01    
    ledmatrix().faceplate_show(0, 0, *show_face)
    codey.color_off()
    return True

def game_over_check():
    global current_backgroup

def on_start_callback():
    global game_status
    global run_speed
    global user_score
    count = 0
    while True:
        speed_control()
        if game_status == GAME_READY:
            if codey.is_button("C"):
                game_status = GAME_PLAYING

        elif game_status == GAME_PLAYING:
            if count % run_speed == 0:
                if update_background():
                	    pass
                else:
                    game_status = GAME_OVER

        elif game_status == GAME_OVER:
            codey.show(user_score)
            game_status = GAME_READY
            game_init()

        elif game_status == GAME_PASS:
            game_status = GAME_PLAYING

        game_over_check()
        time.sleep(0.01)
        count += 1
codey.on_start(on_start_callback)

def on_button_callback():
    global current_backgroup
    global note_play_index
    global update_row_num
    global game_status
    global user_score
    if game_status != GAME_PLAYING:
        pass
    else:
        index = update_row_num // 3 - 2
        print('A index is', index)
        if current_backgroup[NOTE_LEFT_COLUMN] & 0x01:
            codey.green(50)
            user_score += 1
            codey.play_note(note_table[index][0], note_table[index][1])

codey.on_button('A', on_button_callback)

def on_button1_callback():
    global current_backgroup
    global note_play_index
    global update_row_num
    global user_score

    if game_status != GAME_PLAYING:
        pass
    else:
        index =  update_row_num // 3 - 2
        print('B index is', index)
        if current_backgroup[NOTE_RIGHT_COLUMN] & 0x01:
            codey.green(50)
            user_score += 1
            codey.play_note(note_table[index][0], note_table[index][1])

codey.on_button('B', on_button1_callback)

def on_button2_callback():
    global current_backgroup
    global note_play_index
    global update_row_num
    global user_score
    if game_status != GAME_PLAYING:
        pass
    else:
        index =  update_row_num // 3 - 2
        print('C index is', index)
        if current_backgroup[NOTE_MIDDLE_COLUMN] & 0x01:
            codey.green(50)
            user_score += 1
            codey.play_note(note_table[index][0], note_table[index][1])

codey.on_button('C', on_button2_callback)