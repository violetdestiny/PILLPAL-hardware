import RPi.GPIO as GPIO
import time

class Hardware:
    def __init__(self, reed_pin=23, led_pin=18, motor_pin=12, buzzer_pin=16):
        self.reed_pin = reed_pin
        self.led_pin = led_pin
        self.motor_pin = motor_pin
        self.buzzer_pin = buzzer_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.reed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.buzzer_pin, GPIO.OUT, initial=GPIO.LOW)

    def led_on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(self.led_pin, GPIO.LOW)

    def motor_on(self):
        GPIO.output(self.motor_pin, GPIO.HIGH)

    def motor_off(self):
        GPIO.output(self.motor_pin, GPIO.LOW)

    def buzzer_on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def buzzer_off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def reed_is_open(self):
        return GPIO.input(self.reed_pin) == GPIO.HIGH

    def cleanup(self):
        GPIO.cleanup()
