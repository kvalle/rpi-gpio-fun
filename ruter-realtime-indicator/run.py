#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio
import time

import display
import ruter
import config

mode = 0
stops = [
    u"57 Carl Berners plass",
    u"57 Økern T"
]
buttons = [18, 16]
leds = [10, 8]

minutes = {}

## Code for updating everything

def refresh_ruter_data():
    global minutes
    minutes = ruter.minutes_until_next(config.stop_id)

    for dest, mins in minutes.iteritems():
        print "[{:2d} min] {}".format(mins, dest.encode('UTF-8'))
    print

def update_display(index):
    stop = stops[index]
    display.set_number(minutes[stop] if stop in minutes else 1000)

def update():
    update_display(mode)
    set_mode_led(mode)

## Code for reacting to button press

def set_mode(channel):
    global mode
    mode = buttons.index(channel)
    update()

def set_mode_led(mode):
    for i, pin in enumerate(leds):
        gpio.output(pin, gpio.HIGH if i == mode else gpio.LOW)

## Housekeeping methods

def setup():
    gpio.setmode(gpio.BOARD)

    display.setup()

    gpio.setup(leds, gpio.OUT)
    gpio.output(leds, gpio.LOW)

    gpio.setup(buttons, gpio.IN, pull_up_down=gpio.PUD_UP)
    for pin in buttons:
        gpio.add_event_detect(pin, gpio.FALLING, bouncetime=200)
        gpio.add_event_callback(pin, set_mode)

    set_mode_led(mode)

def cleanup():
    display.cleanup()
    warnings.simplefilter("ignore")
    gpio.cleanup()
    warnings.resetwarnings()

def main():
    setup()

    try:
        while True:
            refresh_ruter_data()
            update_display(mode)
            time.sleep(15)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

    print "> Bye :)"

if __name__ == "__main__":
    main()
