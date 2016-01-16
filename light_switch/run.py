from time import sleep
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(light, GPIO.OUT, initial=GPIO.LOW)

def toggle(light):
    GPIO.output(light, not GPIO.input(light))

if __name__ == '__main__':
    button = 7
    light = 11
    
    setup()
    
    try:
        while True:
            input_state = GPIO.input(button)
            if input_state == False:
                toggle(light)
                sleep(.2)
    except:
        GPIO.cleanup()

