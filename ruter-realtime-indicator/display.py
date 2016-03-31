#!/usr/bin/env python
# encoding: UTF-8

import warnings
import RPi.GPIO as gpio
import time

# shift register
ds    = 24
clock = 26
latch = 22

# LEDs
led_10s_mapping = {
    # mapping from pin number to when to light
    13: 10,
    15: 20,
    19: 30,
    21: 40,
    23: 50
}
led_10s_pins = led_10s_mapping.keys()

## "public" methods

def setup():
    gpio.setmode(gpio.BOARD)
    
    gpio.setup([ds, clock, latch], gpio.OUT)
    gpio.output([ds, clock, latch], gpio.LOW)

    gpio.setup(led_10s_pins, gpio.OUT)
    gpio.output(led_10s_pins, gpio.LOW)

def cleanup():
    warnings.simplefilter("ignore")
    gpio.cleanup()
    warnings.resetwarnings()

def set_number(num):
    if num > 59:
        set_hightest_led()
        set_display_value(0)
    else:
        set_led_number(num)
        set_display_number(num % 10)

## Code for driving the five 10-indicator LEDs

def set_hightest_led():
    for pin, limit in led_10s_mapping.iteritems():
        gpio.output(pin, gpio.HIGH if limit >= 50 else gpio.LOW)

def set_led_number(num):
    for pin, limit in led_10s_mapping.iteritems():
        gpio.output(pin, gpio.HIGH if num >= limit else gpio.LOW)

## Code for driving 7-segment display

def tick(pin):
    gpio.output(pin, gpio.HIGH)
    time.sleep(0.01)
    gpio.output(pin, gpio.LOW)

def set_display_value(value):
    for i in range(8):
        bitwise=0x80>>i
        val = gpio.HIGH if bitwise&value else gpio.LOW
        gpio.output(ds, val)
        tick(clock)
    tick(latch)

def set_display_number(num):
    # individual segments' active bits
    a   = 4   # 0b00000100
    b   = 8   # 0b00001000
    c   = 64  # 0b01000000
    d   = 32  # 0b00100000
    e   = 16  # 0b00010000
    f   = 2   # 0b00000010
    g   = 1   # 0b00000001
    dot = 128 # 0b10000000

    # bit-patterns for activating correct segments
    # to form the right number shapes
    numbers = {
        0: a | b | c | d | e | f,
        1: b | c,
        2: a | b | g | e | d,
        3: a | b | c | d | g,
        4: b | c | f | g,
        5: a | c | d | f | g,
        6: a | c | d | e | f | g,
        7: a | b | c,
        8: a | b | c | d | e | f | g,
        9: a | b | c | d | f | g
    }

    set_display_value(numbers[num])


## Some demonstration code, in case someone runs 
## this module directly

def main():
    setup()
    try:
        for i in range(60):
            print i
            set_number(i)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

    print "> Bye :)"

if __name__=="__main__":
    main()
