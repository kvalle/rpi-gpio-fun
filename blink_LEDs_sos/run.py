from time import sleep
import RPi.GPIO as GPIO

green = 13
yellow = 15
red = 16

def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(yellow, GPIO.OUT)
    GPIO.setup(red, GPIO.OUT)

def blink(lights, t=0.2):
    for light in lights:
        GPIO.output(light, False)
    sleep(t)
    for light in lights:
        GPIO.output(light, True)
    sleep(t)

def sos(lights):
    [blink(lights, .2) for _ in range(3)]
    sleep(.2)
    [blink(lights, .4) for _ in range(3)]
    sleep(.2)
    [blink(lights, .2) for _ in range(3)]
    sleep(2)

if __name__ == '__main__':
    setup()
        
    try:
        while True:
            sos([green, yellow, red])
            sos([green])
            sos([yellow])
            sos([red])
    except KeyboardInterrupt:
        GPIO.cleanup()
