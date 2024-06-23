import digitalio
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

print("== Pi Pico multifunction knob 1.0 ==")

CLK_PIN = board.GP4
DT_PIN = board.GP3
SW_PIN = board.GP2
clk_last = None
count = 0
totalMode = 5
currentMode = 0

cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)


clk = digitalio.DigitalInOut(CLK_PIN)
clk.direction = digitalio.Direction.INPUT

dt = digitalio.DigitalInOut(DT_PIN)
dt.direction = digitalio.Direction.INPUT

sw = digitalio.DigitalInOut(SW_PIN)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

def millis():
    return time.monotonic() * 1000

def ccw():
    print("CCW")
    
    if (currentMode == 0):    #brightness down
        cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
        
    elif(currentMode ==2):    #scroll down
        keyboard.press(Keycode.DOWN_ARROW)
        mouse.move(wheel=-1)
        keyboard.release(Keycode.DOWN_ARROW)

    elif(currentMode == 1):   # Volume decrement
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        
    elif(currentMode == 3):
        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        
    elif(currentMode == 4):
        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
    
        
def cw():
    print("CW")
    if (currentMode == 0):     #  brightness up
        cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)             
        
    elif(currentMode ==2):     # horizontal scroll left
        keyboard.press(Keycode.UP_ARROW)
        mouse.move(wheel=1)
        keyboard.release(Keycode.UP_ARROW)
   
    elif(currentMode == 1):     # Volume increment
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        
    elif(currentMode == 3):
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
    
    

        
def long_press():
    #Close Window: ALT+F4
    keyboard.press(Keycode.ALT, Keycode.F4)  
    cc.send(ConsumerControlCode.EJECT)
    keyboard.release_all()

while(1):
    clkState = clk.value
    if(clk_last !=  clkState):
        if(dt.value != clkState):
            cw()
        else:
            ccw()
            
    if (sw.value == 0):
        pressTime = millis()
        time.sleep(0.2)
        longPress = False
        
        while(sw.value == 0):
            if(millis() - pressTime > 1000 and not longPress):
                print("longPress")
                longPress = True
                long_press()
                

        if (not longPress):
            currentMode += 1
            currentMode %= totalMode
            print("Mode: " + str(currentMode))
            
    clk_last = clkState
    