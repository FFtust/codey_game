import codey
import time
import random
import rocky

BATTERY_LOW_PERCENT = 30
angerValue = 0

def on_message_callback():
    global angerValue
    while True:
        codey.face('00003c7e7e3c000000003c7e7e3c0000')
        time.sleep(float(random.randint(2, 6)))
        codey.face('0000183c3c1800000000183c3c180000')
        time.sleep(float(random.uniform(0, 0.05)))
        codey.face('00000808080800000000080808080000')
        time.sleep(float(random.uniform(0.1, 0.3)))
        codey.face('0000183c3c1800000000183c3c180000')
        time.sleep(float(random.uniform(0, 0.05)))


codey.on_message(str('hello'), on_message_callback)

def on_button_callback():
    global angerValue
    if angerValue > random.randint(3, 5):
        angerValue = 0
        time.sleep(0.2)
        codey.face('00003c1e0e0400000000040e1e3c0000')
        rocky.back(50)
        time.sleep(0.4)
        codey.say('dog.wav')
        codey.face('00007c3e1e0e040000040e1e3e7c0000')
        rocky.back(100)
        time.sleep(0.05)
        rocky.forward(100)
        time.sleep(0.5)
        rocky.back(100)
        time.sleep(0.01)
        rocky.stop()
        time.sleep(0.2)

    else:
        codey.say('wrong.wav')
        codey.face('00081c1c3c3820000020383c1c1c0800')
        time.sleep(0.3)
        rocky.back(20)
        codey.face('00040e0e1e1c100000101c1e0e0e0400')
        rocky.back(50)
        time.sleep(0.1)
        codey.face('00081c1c3c3820000020383c1c1c0800')
        rocky.stop()
        time.sleep(0.3)
        codey.face('00183c3c7c7820000020787c3c3c1800')
        time.sleep(0.1)
        codey.face('00003c7e7e3c000000003c7e7e3c0000')
        angerValue = (angerValue if isinstance(angerValue, int) or isinstance(angerValue, float) else 0) + 1

    codey.message(str('hello'))

codey.on_button('C', on_button_callback)

def on_button1_callback():
    global angerValue
    if angerValue > random.randint(3, 5):
        angerValue = 0
        time.sleep(0.2)
        codey.face('00003c1e0e0400000000040e1e3c0000')
        rocky.back(50)
        time.sleep(0.4)
        codey.say('dog.wav')
        codey.face('00007c3e1e0e040000040e1e3e7c0000')
        rocky.back(100)
        time.sleep(0.05)
        rocky.forward(100)
        time.sleep(0.5)
        rocky.back(100)
        time.sleep(0.01)
        rocky.stop()
        time.sleep(0.2)

    else:
        codey.say('happy.wav')
        codey.face('000c18181c0c000000000c1c18180c00')
        time.sleep(0.3)
        rocky.left(70)
        time.sleep(0.05)
        codey.face('00183030381800000000183830301800')
        rocky.right(70)
        time.sleep(0.05)
        rocky.left(70)
        time.sleep(0.05)
        rocky.right(70)
        time.sleep(0.05)
        rocky.stop()
        codey.face('000c18181c0c000000000c1c18180c00')
        time.sleep(0.3)
        codey.face('00183030381800000000183830301800')
        time.sleep(0.1)
        codey.face('00003c7e7e3c000000003c7e7e3c0000')
        angerValue = (angerValue if isinstance(angerValue, int) or isinstance(angerValue, float) else 0) + 1

    codey.message(str('hello'))

codey.on_button('A', on_button1_callback)

def on_button2_callback():
    global angerValue
    if angerValue > random.randint(3, 5):
        angerValue = 0
        time.sleep(0.2)
        codey.face('00003c1e0e0400000000040e1e3c0000')
        rocky.back(50)
        time.sleep(0.4)
        codey.say('dog.wav')
        codey.face('00007c3e1e0e040000040e1e3e7c0000')
        rocky.back(100)
        time.sleep(0.05)
        rocky.forward(100)
        time.sleep(0.5)
        rocky.back(100)
        time.sleep(0.01)
        rocky.stop()
        time.sleep(0.2)

    else:
        codey.say('happy.wav')
        codey.face('000c18181c0c000000000c1c18180c00')
        time.sleep(0.3)
        rocky.right(70)
        time.sleep(0.05)
        codey.face('00183030381800000000183830301800')
        rocky.left(70)
        time.sleep(0.05)
        rocky.right(70)
        time.sleep(0.05)
        rocky.left(70)
        time.sleep(0.05)
        rocky.stop()
        codey.face('000c18181c0c000000000c1c18180c00')
        time.sleep(0.3)
        codey.face('00183030381800000000183830301800')
        time.sleep(0.1)
        codey.face('00003c7e7e3c000000003c7e7e3c0000')
        angerValue = (angerValue if isinstance(angerValue, int) or isinstance(angerValue, float) else 0) + 1
        codey.message(str('hello'))


codey.on_button('B', on_button2_callback)


angerValue = 0
while True:
    cap = codey.get_battery_capacity()
    if cap >= BATTERY_LOW_PERCENT:
        codey.face('00003c7e7e3c000000003c7e7e3c0000')
        time.sleep(float(random.randint(2, 6)))
        codey.face('0000181c1c1800000000181c1c180000')
        time.sleep(float(random.uniform(0, 0.05)))
        codey.face('00000808080800000000080808080000')
        time.sleep(float(random.uniform(0.1, 0.3)))
        codey.face('0000183c3c1800000000183c3c180000')
        time.sleep(float(random.uniform(0, 0.05)))
    else:
        codey.color('#ff0000')
        codey.face('0000007e7e7e424242427e7e18000000', 1)
        codey.color('#000000')
        codey.face('00000c1e3e3c000000003c3e1e0c0000', 0.3)
        codey.face('000c1e3e3c000000003c3e1e0c000000', 0.1)
        codey.face('0000000c1e3e3c000000003c3e1e0c00', 0.1)
        codey.face('00000c1e3e3c000000003c3e1e0c0000', 0.3)
    time.sleep(0.1)
