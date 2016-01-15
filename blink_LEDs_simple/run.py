from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

green = 13
yellow = 15
red = 16

GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

def blink(light, t=0.2):
	GPIO.output(light, False)
	sleep(t)
	GPIO.output(light, True)
	sleep(t)

if __name__ == '__main__':
	try:
        	while True:
			blink(green)
			blink(yellow)
			blink(red)
			blink(yellow)
	except:
		GPIO.cleanup()

