import RPi.GPIO as GPIO
import time

LED_PIN = 18
LED_GND_PIN = 15
BUZZER_PIN = 21
MOTOR_PIN = 12

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_GND_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

led_pwm = GPIO.PWM(LED_PIN, 500)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
motor_pwm = GPIO.PWM(MOTOR_PIN, 200)

led_pwm.start(0)
buzzer_pwm.start(0)
motor_pwm.start(0)

NOTES = {
    "C5": 523,
    "E5": 659,
    "G5": 784,
    "R": 0
}

MELODY = [
    ("C5", 0.15), ("R", 0.05),
    ("E5", 0.15), ("G5", 0.15)
]

def play_melody():
    for note, duration in MELODY:
        freq = NOTES[note]
        if freq == 0:
            buzzer_pwm.ChangeDutyCycle(0)
        else:
            buzzer_pwm.ChangeFrequency(freq)
            buzzer_pwm.ChangeDutyCycle(60)
        time.sleep(duration)
    buzzer_pwm.ChangeDutyCycle(0)

def turn_led(on=True):
    if on:
        GPIO.output(LED_GND_PIN, GPIO.LOW)
        for duty in range(0, 101, 3):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(0.01)
    else:
        led_pwm.ChangeDutyCycle(0)
        GPIO.output(LED_GND_PIN, GPIO.HIGH)

def vibrate(on=True):
    if on:
        motor_pwm.ChangeDutyCycle(75)
    else:
        motor_pwm.ChangeDutyCycle(0)

def alert_start():
    turn_led(True)
    vibrate(True)
    buzzer_pwm.ChangeFrequency(800)
    buzzer_pwm.ChangeDutyCycle(50)

def alert_stop():
    turn_led(False)
    vibrate(False)
    buzzer_pwm.ChangeDutyCycle(0)

def cleanup():
    led_pwm.stop()
    buzzer_pwm.stop()
    motor_pwm.stop()
    GPIO.cleanup()
