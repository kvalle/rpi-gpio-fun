#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio
import time

import display
import ruter
import config

# The list of destinations, and which index is currently active
destinations = config.destinations
active_index = 0

# Pin assignments for buttons and LEDs
# Same order as list of destinations
buttons = [18, 16]
leds = [10, 8]

# Cache for number of minutes until next departure
minutes = [None, None]


## Code for updating everything

def refresh_ruter_data():
    global minutes
    try:
        departures = ruter.get_data(config.stop_id)
        for index, dests in enumerate(destinations):
            departure_times = [dep["wait"]
                                for dep in departures
                                if dep["destination"] in dests]
            minutes[index] = min(departure_times) if departure_times else None
            
            print dests
            print "   ", departure_times
    except ruter.RuterConnectionException, e:
        print e
        minutes = [-1, -1]

def update_display():
    if None == minutes[active_index]:
        display.set_char('H')
    else:
        display.set_number(minutes[active_index])

def update():
    update_display()
    set_active_destination_led()

## Code for reacting to button press

def set_active_destination(channel):
    global active_index
    active_index = buttons.index(channel)
    update()

def set_active_destination_led():
    for i, pin in enumerate(leds):
        gpio.output(pin, gpio.HIGH if i == active_index else gpio.LOW)

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
    except Exception, e:
        print "System fuckup: " + str(e)
        print "Aborted."
    finally:
        cleanup()

    print "> Bye :)"

if __name__ == "__main__":
    main()
