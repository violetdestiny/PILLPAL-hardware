import RPi.GPIO as GPIO
import time

LID_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LID_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def lid_is_open():
    return GPIO.input(LID_PIN) == GPIO.HIGH

def detect_lid_events(on_open, on_close):
    last_state = lid_is_open()

    while True:
        current_state = lid_is_open()

        if current_state != last_state:
            if current_state:
                on_open()
            else:
                on_close()

        last_state = current_state
        time.sleep(0.1)
