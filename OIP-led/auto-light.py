import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)

detector = 6
GPIO.setup(detector, GPIO.IN)

while True:
    state = GPIO.input(detector)
    GPIO.output(led, not state)
    time.sleep(0.01)