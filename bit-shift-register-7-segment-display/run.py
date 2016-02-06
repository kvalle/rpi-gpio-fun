# encoding: UTF-8

import RPi.GPIO as gpio
from time import sleep

ds=24
clock=26
latch=22

pause=0.1

def setup():
    gpio.setmode(gpio.BOARD)

    gpio.setup([ds, clock, latch], gpio.OUT)
    gpio.output([ds, clock, latch], gpio.LOW)

def cleanup():
    gpio.output([ds, clock, latch], gpio.LOW)
    gpio.cleanup()

def tick(pin):
    gpio.output(pin, gpio.HIGH)
    sleep(0.1)
    gpio.output(pin, gpio.LOW)

def set_value(value):
    for i in range(8):
        bitwise=0x80>>i
        val = gpio.HIGH if bitwise&value else gpio.LOW
        gpio.output(ds, val)
        tick(clock)
    tick(latch)

def set_number(num):
    # individual segments
    a   = 4   # 0b00000100
    b   = 8   # 0b00001000
    c   = 64  # 0b01000000
    d   = 32  # 0b00100000
    e   = 16  # 0b00010000
    f   = 2   # 0b00000010
    g   = 1   # 0b00000001
    dot = 128 # 0b10000000

    # connecting segments to number shapes
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

    set_value(numbers[num])

def main():
    setup()
    try:
        while True:
            for i in range(10):
                set_number(i)
                sleep(.5)

    except KeyboardInterrupt:
        print "EXIT"
        set_value(0)
        cleanup()

if __name__=="__main__":
    main()
