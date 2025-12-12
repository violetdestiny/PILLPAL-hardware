import RPi.GPIO as GPIO
import time
import threading

LED_PIN = 18
LED_GND_PIN = 15
BUZZER_PIN = 21

# MOTOR REMOVED (disabled completely)
# MOTOR_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_GND_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# DO NOT INITIALIZE PWM UNTIL NEEDED
led_pwm = None
buzzer_pwm = None

# motor_pwm = None   # REMOVED

alarm_active = False
pref_sound = True
pref_led = True
# pref_vibration = False   # REMOVED


def ensure_pwm():
    """Initialize PWM ONLY when needed (prevents startup pulses)."""
    global led_pwm, buzzer_pwm

    if led_pwm is None:
        led_pwm = GPIO.PWM(LED_PIN, 500)
        led_pwm.start(0)

    if buzzer_pwm is None:
        buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
        buzzer_pwm.start(0)

    # MOTOR REMOVED
    # if motor_pwm is None:
    #     motor_pwm = GPIO.PWM(MOTOR_PIN, 200)
    #     motor_pwm.start(0)


def led_effect():
    for duty in range(0, 100, 5):
        if not alarm_active or not pref_led:
            led_pwm.ChangeDutyCycle(0)
            return
        led_pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)

    for duty in range(100, 0, -5):
        if not alarm_active or not pref_led:
            led_pwm.ChangeDutyCycle(0)
            return
        led_pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)


def alarm_loop():
    global alarm_active

    ensure_pwm()

    while alarm_active:
        # LED effect
        if pref_led:
            GPIO.output(LED_GND_PIN, GPIO.LOW)
            led_effect()
        else:
            led_pwm.ChangeDutyCycle(0)
            GPIO.output(LED_GND_PIN, GPIO.HIGH)

        # BUZZER sound
        if pref_sound:
            buzzer_pwm.ChangeFrequency(800)
            buzzer_pwm.ChangeDutyCycle(60)
        else:
            buzzer_pwm.ChangeDutyCycle(0)

        # MOTOR VIBRATION REMOVED
        # if pref_vibration:
        #     motor_pwm.ChangeDutyCycle(80)
        # else:
        #     motor_pwm.ChangeDutyCycle(0)

        time.sleep(0.3)

        buzzer_pwm.ChangeDutyCycle(0)
        # motor_pwm.ChangeDutyCycle(0)   # REMOVED
        time.sleep(0.2)


def alert_start(sound=True, vibration=False, led=True):
    """Start alarm (vibration ignored because motor removed)."""
    global alarm_active, pref_sound, pref_led

    pref_sound = sound
    pref_led = led
    # pref_vibration = False   # REMOVED

    if alarm_active:
        return

    alarm_active = True
    ensure_pwm()

    t = threading.Thread(target=alarm_loop)
    t.daemon = True
    t.start()


def alert_stop():
    global alarm_active

    alarm_active = False

    if led_pwm:
        led_pwm.ChangeDutyCycle(0)
    if buzzer_pwm:
        buzzer_pwm.ChangeDutyCycle(0)
    # if motor_pwm:
    #     motor_pwm.ChangeDutyCycle(0)

    GPIO.output(LED_GND_PIN, GPIO.HIGH)
    time.sleep(0.1)


def cleanup():
    global alarm_active
    alarm_active = False

    if led_pwm:
        led_pwm.stop()
    if buzzer_pwm:
        buzzer_pwm.stop()
    # if motor_pwm:
    #     motor_pwm.stop()

    GPIO.cleanup()
