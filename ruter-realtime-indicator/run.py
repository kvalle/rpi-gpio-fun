#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio

import display

mode = 0

# buttons
buttons = [18, 16]
mode1_btn = 18
mode2_btn = 16

# LEDs
leds = [10, 8]
mode1_led = 10
mode2_led = 8

def set_mode_led(mode):
    for i, pin in enumerate(leds):
        gpio.output(pin, gpio.HIGH if i == mode else gpio.LOW)

def set_mode(channel):
    mode = buttons.index(channel)
    set_mode_led(mode)

def setup():
    gpio.setmode(gpio.BOARD)

    display.setup()

    gpio.setup(leds, gpio.OUT)
    gpio.output(leds, gpio.LOW)

    gpio.setup(buttons, gpio.IN, pull_up_down=gpio.PUD_UP)
    for pin in buttons:
        gpio.add_event_detect(pin, gpio.RISING, bouncetime=200)
        gpio.add_event_callback(pin, set_mode)

def cleanup():
    display.cleanup()
    warnings.simplefilter("ignore")
    gpio.cleanup()
    warnings.resetwarnings()

def main():
    setup()

    try:
        #display.set_number(0)
        set_mode_led(mode)
        raw_input("Press ENTER to exit")
    finally:
        cleanup()

    print "> Bye :)"

if __name__=="__main__":
    main()
