import RPi.GPIO as GPIO
import time

BUZZER = 21  

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
pwm = GPIO.PWM(BUZZER, 440)
pwm.start(0)


notes = {
    "C5": 523,
    "B4": 494,
    "A4": 440,
    "G4": 392,
    "G5": 784, 
    "E5": 659,
    "D5": 587,
    "E4": 330,
    "F5": 698,
    "A5": 880,
    "R": 0
}

melody = [
    ("E5",0.15), ("E5",0.15), ("R",0.1),
    ("E5",0.15), ("R",0.1),
    ("C5",0.15), ("E5",0.15), ("G5",0.3),
    ("R",0.2),
    ("G4",0.15), ("R",0.15),

    ("C5",0.2), ("R",0.05),
    ("G4",0.2), ("R",0.05),
    ("E4",0.2), ("R",0.05),
    ("A4",0.2), ("R",0.05),
    ("B4",0.2), ("R",0.05),
    ("A4",0.2),
    ("G4",0.15), ("E5",0.15),
    ("G5",0.15), ("A5",0.25),

    ("F5",0.2), ("G5",0.2), ("R",0.1),
    ("E5",0.2), ("C5",0.2),
    ("D5",0.2), ("B4",0.25),

    ("E5",0.15), ("E5",0.15), ("R",0.1),
    ("E5",0.15), ("R",0.1),
    ("C5",0.15), ("E5",0.15), ("G5",0.3),
    ("R",0.2),
]

def play(note, dur):
    freq = notes[note]
    if freq == 0:
        pwm.ChangeDutyCycle(0)
        time.sleep(dur)
        return
    pwm.ChangeFrequency(freq)
    pwm.ChangeDutyCycle(50)
    time.sleep(dur)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.04)

try:
    print("Mario Theme — 30 seconds")

    start = time.time()
    while time.time() - start < 30:
        for n, d in melody:
            play(n, d)
            if time.time() - start >= 30:
                break

finally:
    pwm.stop()
    GPIO.cleanup()
    print("Done.")
