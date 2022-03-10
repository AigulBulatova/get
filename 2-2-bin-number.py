import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
number = []

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

number = [0, 0, 0, 0, 0, 0, 0, 1]

GPIO.output (dac, number)

time.sleep(15)

GPIO.output (dac, 0)

GPIO.cleanup() 