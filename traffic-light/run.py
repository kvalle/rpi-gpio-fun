#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    lights = [white, green, yellow, red]
    GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)

toggle = lambda pin: GPIO.output(pin, not GPIO.input(pin))
off    = lambda pin: GPIO.output(pin, GPIO.LOW)
on     = lambda pin: GPIO.output(pin, GPIO.HIGH)

def light(pin, duration=1):
    on(pin)
    sleep(duration)
    off(pin)

def walk():
    off(green)
    light(yellow)
    on(red)
    sleep(1)
    on(white)

def drive():
    off(white)
    sleep(1)
    off(red)
    light(yellow)
    on(green)

if __name__ == '__main__':
    button = 7
    white = 8
    green = 16
    yellow = 18
    red = 22
    
    setup()
    
    try:
        on(green)

        while True:
            input_state = GPIO.input(button)
            if input_state == False:
                walk()
                sleep(5)
                drive()
    except:
        GPIO.cleanup()

