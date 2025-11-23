import RPi.GPIO as GPIO
import time

A = 15  
B = 18  

GPIO.setmode(GPIO.BCM)

GPIO.setup(A, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(B, GPIO.OUT, initial=GPIO.LOW)

pwm = GPIO.PWM(B, 500)  
pwm.start(0)            

try:
    print("FADE-IN...")
    for duty in range(0, 101, 2):  
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.03)

    print("LED ON 10 secs...")
    time.sleep(10)

    print("OFF LED...")
    pwm.ChangeDutyCycle(0)
    time.sleep(0.3)

finally:
    pwm.stop()
    GPIO.cleanup()
