from time import sleep
import RPi.GPIO as GPIO

def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
            
    for light in [green, yellow, red]:
        GPIO.setup(light, GPIO.OUT)
        GPIO.output(light, False)

def blink(light, t=0.2):
	GPIO.output(light, True)
	sleep(t)
	GPIO.output(light, False)
	sleep(t)

if __name__ == '__main__':
    green = 13
    yellow = 15
    red = 16
    
    setup()
    
    try:
        while True:
            blink(green)
            blink(yellow)
            blink(red)
            blink(yellow)
    except:
        GPIO.cleanup()

