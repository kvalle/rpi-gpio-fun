#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio
import time

import display
import ruter
import config

# The list of destinations, and which one is active
destinations = config.destinations
active_destination = destinations[0]

# Pin assignments for buttons and LEDs
# Same order as list of destinations
buttons = [18, 16]
leds = [10, 8]

# Cache for number of minutes until next departures
minutes = { 
    dest: None 
    for dest in destinations
}


## Code for updating everything

def refresh_ruter_data():
    global minutes
    try:
        next = ruter.minutes_until_next(config.stop_id)
        minutes = {
            dest: next[dest] if dest in next else None
            for dest in destinations
        }
    except ruter.RuterConnectionException, e:
        minutes = None

    print_minutes(minutes)

def print_minutes(minutes):
    if not minutes:
        print "Unable to retrieve transit data."
    else:
        for dest in destinations:
            mins = minutes[dest]
            msg = "[{:2d} min]".format(mins) if mins else "[ long ]"
            msg += " {}".format(dest.encode('UTF-8'))
            print msg


def update_display():
    if not minutes:
        display.set_char('E')
    else:
        if not minutes[active_destination]:
            display.set_char('H')
        else:
            mins = minutes[active_destination] 
            display.set_number(mins)

def update():
    update_display()
    set_active_destination_led()

## Code for reacting to button press

def set_active_destination(channel):
    global active_destination
    index = buttons.index(channel)
    active_destination = destinations[index]
    update()

def set_active_destination_led():
    index = destinations.index(active_destination)
    for i, pin in enumerate(leds):
        gpio.output(pin, gpio.HIGH if i == index else gpio.LOW)

## Housekeeping methods

def setup():
    gpio.setmode(gpio.BOARD)

    display.setup()

    gpio.setup(leds, gpio.OUT)
    gpio.output(leds, gpio.LOW)

    gpio.setup(buttons, gpio.IN, pull_up_down=gpio.PUD_UP)
    for pin in buttons:
        gpio.add_event_detect(pin, gpio.FALLING, bouncetime=200)
        gpio.add_event_callback(pin, set_active_destination)

    set_active_destination_led()

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
            update_display()
            time.sleep(15)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

    print "> Bye :)"

if __name__ == "__main__":
    main()
