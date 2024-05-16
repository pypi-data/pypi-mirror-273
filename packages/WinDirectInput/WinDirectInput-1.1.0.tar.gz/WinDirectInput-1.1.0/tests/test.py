import time
import directinput_v2 as di

time.sleep(2)
with di.keyHold('ctrl', 'shift'):
    di.keyPress('esc')
