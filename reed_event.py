import RPi.GPIO as GPIO
import time

REED = 23 

GPIO.setmode(GPIO.BCM)
GPIO.setup(REED, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Reading reed switch every 100ms... Press Ctrl+C to exit.")

try:
    while True:
        v = GPIO.input(REED)
        if v == 1:
            print("OPEN")
        else:
            print("CLOSED")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
