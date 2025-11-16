import RPi.GPIO as GPIO
import time

LID_PIN = 23 

GPIO.setmode(GPIO.BCM)
GPIO.setup(LID_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_lid_open():
  
    return GPIO.input(LID_PIN) == GPIO.LOW

def detect_lid_open(callback):
    last_state = is_lid_open()
    while True:
        current_state = is_lid_open()
        if current_state != last_state:
            if current_state:
                callback()
        last_state = current_state
        time.sleep(0.1)
