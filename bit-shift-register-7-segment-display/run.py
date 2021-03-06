# encoding: UTF-8

import RPi.GPIO as gpio
from time import sleep

# shift register
ds    = 24
clock = 26
latch = 22

# buttons
inc   = 18
count = 16

# waiting time for clock pulse
pause=0.1

# variable for keeping track of what to show next
counter = 0

def setup():
    gpio.setmode(gpio.BOARD)

    gpio.setup([ds, clock, latch], gpio.OUT)
    gpio.output([ds, clock, latch], gpio.LOW)

    gpio.setup([inc, count], gpio.IN, pull_up_down=gpio.PUD_UP)

def tick(pin):
    gpio.output(pin, gpio.HIGH)
    sleep(0.01)
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

def increment(channel):
    global counter
    counter = (counter + 1) % 10

def display_count(channel):
    global counter
    set_number(counter)
    counter = 0

def main():
    setup()

    gpio.add_event_detect(inc, gpio.RISING, bouncetime=200)
    gpio.add_event_callback(inc, increment)

    gpio.add_event_detect(count, gpio.RISING, bouncetime=200)
    gpio.add_event_callback(count, display_count)

    try:
        while True:
            sleep(1)

    except KeyboardInterrupt:
        gpio.cleanup()

    print "done"

if __name__=="__main__":
    main()
