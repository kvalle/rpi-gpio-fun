#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

def setup(light):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light, GPIO.OUT, initial=GPIO.LOW)

if __name__ == '__main__':
    led = 8
    setup(led)

    pwm = GPIO.PWM(led, 50)
    pwm.start(5)
    
    try:
        while True:
            for dc in range(5, 101, 5) + range(100, 5, -5):
                pwm.ChangeDutyCycle(dc)
                sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

