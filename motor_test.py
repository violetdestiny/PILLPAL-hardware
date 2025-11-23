import RPi.GPIO as GPIO
import time

MOTOR_PIN = 12 


GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

try:
    print("Vibrate 4 secs...")
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    time.sleep(4)
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    print("done")

finally:
    GPIO.cleanup()
