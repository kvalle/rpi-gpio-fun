#!/usr/bin/env python

import random
from time import sleep

import RPi.GPIO as GPIO

def display(counter):
    GPIO.output(leds, num[counter])

def setup(lights):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)

def next(links, current, history, bad):
    possible = links[current]

    # a
    # b
    # g
    # e
    # f
    # a

    # current = e
    # history = [g, b]

    if len(history) > 0 and history[0] in possible:
        possible.remove(history[0])

    for b in bad:
        if history[:2] == bad[b] and b in possible:
            possible.remove(b)

    return random.choice(possible)

if __name__ == '__main__':
    a, b, c, d, e, f, g = 21, 23, 24, 22, 18, 19, 15
    #a, b, c, d, e, f, g = "a", "b", "c", "d", "e", "f", "g"
    leds = [a, b, c, d, e, f, g]

    links = {
        a: [f, b],
        b: [a, c, g],
        c: [b, d, g],
        d: [c, e],
        e: [d, f, g],
        f: [a, e, g],
        g: [b, c, e, f]
    }

    bad = {
        a: [b, g],
        b: [a, g],
        f: [e, g],
        e: [f, g]
    }

    setup(leds)

    active = g
    history = []
    print active

    try:
        while True:
            history = [active] + history[:4]
            active = next(links, active, history[1:], bad)

            GPIO.output(history[0], GPIO.LOW)
            GPIO.output(active, GPIO.HIGH)
            print active
            sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
