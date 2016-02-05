#!/usr/bin/env python

import RPi.GPIO as GPIO

counter = 0

decrease = 11
increase = 13
buttons = [increase, decrease]

#        a   b   c   d   e   f   g  dp
leds = [21, 23, 24, 22, 18, 19, 15, 26]

num = {  
    #   a  b  c  d  e  f  g  h
    1: [0, 1, 1, 0, 0, 0, 0, 1],
    2: [1, 1, 0, 1, 1, 0, 1, 1],
    3: [1, 1, 1, 1, 0, 0, 1, 1],
    4: [0, 1, 1, 0, 0, 1, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0, 1],
    8: [1, 1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 0, 0, 1, 1, 1],
    0: [1, 1, 1, 1, 1, 1, 0, 1]
}

def display(counter):
    GPIO.output(leds, num[counter])

def button_push(channel):
    global counter

    if channel == increase:
        counter = min(9, counter + 1)
    elif channel == decrease:
        counter = max(0, counter - 1)

    display(counter)

def setup(lights, buttons):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for button in buttons:
        GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(button, button_push)

    GPIO.setup(lights, GPIO.OUT, initial=GPIO.HIGH)

if __name__ == '__main__':
    setup(leds, buttons)
     
    try:
        display(counter)
        raw_input("Press ENTER to exit")
    finally:
        GPIO.cleanup()
