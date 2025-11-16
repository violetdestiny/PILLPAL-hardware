import RPi.GPIO as GPIO

LED_PIN = 18
BUZZER_PIN = 21
MOTOR_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def alert_start(sound=True, vibration=True):
    GPIO.output(LED_PIN, True)
    if sound:
        GPIO.output(BUZZER_PIN, True)
    if vibration:
        GPIO.output(MOTOR_PIN, True)

def alert_stop():
    GPIO.output(LED_PIN, False)
    GPIO.output(BUZZER_PIN, False)
    GPIO.output(MOTOR_PIN, False)
