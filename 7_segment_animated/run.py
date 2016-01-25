#!/usr/bin/env python

import random
from time import sleep

import RPi.GPIO as GPIO

def display(counter):
    GPIO.output(leds, num[counter])

def setup(lights):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)

def next(history, segments):
    next = random.choice([n for n in segments if history in segments[n]])
    return (history[1], next)

if __name__ == '__main__':
    a, b, c, d, e, f, g  =  21,  23,  24,  22,  18,  19,  15
    leds = [a, b, c, d, e, f, g]

    segments = {
        a: [(c, b), (g, b), (e, f), (g, f)],
        b: [(f, a), (d, c), (e, g), (f, g)],
        c: [(a, b), (e, d), (e, g), (f, g)],
        d: [(b, c), (g, c), (f, e), (g, e)],
        e: [(c, d), (a, f), (b, g), (c, g)],
        f: [(b, a), (d, e), (b, g), (c, g)],
        g: [(a, b), (d, c), (d, e), (a, f)]
    }

    setup(leds)

    history = (e, f)
    
    try:
        while True:
            history = next(history, segments)

            GPIO.output(history[0], GPIO.LOW)
            GPIO.output(history[1], GPIO.HIGH)

            sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
