import RPi.GPIO as GPIO
from time import sleep
 
led_port = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_port, GPIO.OUT)

for i in range(10):
    GPIO.output(led_port, GPIO.HIGH)
    print("high")
    sleep(0.5)
    GPIO.output(led_port, GPIO.LOW)
    print("low")
    sleep(0.5)
