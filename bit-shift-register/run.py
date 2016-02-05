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

def number_from_input():
    raw = raw_input("Set a number [0-256]: ")
    try:
        val = int(raw)
        if not 0 <= val <= 256: 
            raise ValueError()
        return val
    except ValueError:
        print "Try again."
        return number_from_input()

def main():
    setup()
    try:
        while True:
            set_value(number_from_input())

    except KeyboardInterrupt:
        print "EXIT"
        set_value(0)
        cleanup()

if __name__=="__main__":
    main()
