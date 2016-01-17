#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

def setup(buttons, lights):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)

toggle = lambda pin: GPIO.output(pin, not GPIO.input(pin))
off    = lambda pin: GPIO.output(pin, GPIO.LOW)
on     = lambda pin: GPIO.output(pin, GPIO.HIGH)

def light(pin, duration=1):
    on(pin)
    sleep(duration)
    off(pin)

def adjust(value, up, pow=1.5):
    value = value * pow if up else value / pow
    value = min(value, 100)
    value = max(value, 1)

    new_direction = up and value < 100 or not up and value == 1
    
    return value, new_direction

if __name__ == '__main__':
    button = 7
    white = 8
    
    setup(button, white)

    pwm = GPIO.PWM(white, 1000)
    pwm.start(0)
    
    brightness = 1
    increase = True
    
    try:
        while True:
            brightness, increase = adjust(brightness, increase)
            pwm.ChangeDutyCycle(brightness)
            sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

