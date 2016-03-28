#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio

import display

# buttons
inc   = 18
count = 16

# variable for keeping track of what to show next
counter = 0

# LEDs
led_dir1 = 10
led_dir2 = 8
led_10 = 13
led_20 = 15
led_30 = 19
led_40 = 21
led_50 = 23

def increment(channel):
    global counter
    counter = (counter + 1) % 10

def display_count(channel):
    global counter
    display.set_number(counter)
    counter = 0

def setup():
    gpio.setmode(gpio.BOARD)

    display.setup()

    gpio.setup([led_dir1, led_dir2], gpio.OUT)
    gpio.output(led_dir2, gpio.LOW)
    gpio.output(led_dir1, gpio.HIGH)

    gpio.setup([inc, count], gpio.IN, pull_up_down=gpio.PUD_UP)

    gpio.add_event_detect(inc, gpio.RISING, bouncetime=200)
    gpio.add_event_callback(inc, increment)

    gpio.add_event_detect(count, gpio.RISING, bouncetime=200)
    gpio.add_event_callback(count, display_count)

def cleanup():
    display.cleanup()
    warnings.simplefilter("ignore")
    gpio.cleanup()
    warnings.resetwarnings()

def main():
    setup()

    try:
        display.set_number(0)
        raw_input("Press ENTER to exit")
    finally:
        cleanup()

    print "> Bye :)"

if __name__=="__main__":
    main()
