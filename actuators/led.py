# actuators/led.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

LED_PIN = 18
LED_GND_PIN = 15

# MQTT setup
BROKER = "localhost"
PORT = 1883
DEVICE_ID = "1"
TOPIC_EVENTS = "pillpal/device/events"

# Create MQTT client for LED events
mqtt_client = mqtt.Client(client_id=f"{DEVICE_ID}_led")
mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_GND_PIN, GPIO.OUT)

# Initialize GND pin to HIGH (off state)
GPIO.output(LED_GND_PIN, GPIO.HIGH)

led_pwm = GPIO.PWM(LED_PIN, 500)
led_pwm.start(0)

def send_led_event(event_type, metadata=None):
    """Send LED event to MQTT and database"""
    payload = {
        "device_id": DEVICE_ID,
        "event_type": event_type,
        "source": "device",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    if metadata:
        payload["metadata"] = metadata

    # Publish to MQTT
    mqtt_client.publish(TOPIC_EVENTS, json.dumps(payload), qos=1)
    print(f"[LED EVENT] {event_type}: {payload}")

def led_on(brightness=100, fade_in=True, log_event=True):
    """Turn LED on with optional fade-in effect"""
    GPIO.output(LED_GND_PIN, GPIO.LOW)
    
    if fade_in:
        for duty in range(0, brightness + 1, 5):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(0.02)
    else:
        led_pwm.ChangeDutyCycle(brightness)
    
    print(f"[LED] ON - brightness: {brightness}%")
    
    if log_event:
        send_led_event("led_activated", {"brightness": brightness, "fade_in": fade_in})

def led_off(fade_out=True, log_event=True):
    """Turn LED off with optional fade-out effect"""
    if fade_out:
        current_duty = led_pwm._duty_cycle
        for duty in range(int(current_duty), -1, -5):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(0.02)
    else:
        led_pwm.ChangeDutyCycle(0)
    
    GPIO.output(LED_GND_PIN, GPIO.HIGH)
    print("[LED] OFF")
    
    if log_event:
        send_led_event("led_deactivated")

def led_blink(times=3, speed=0.5, brightness=100, log_event=True):
    """Blink LED specified number of times"""
    print(f"[LED] Blinking {times} times")
    
    for i in range(times):
        led_on(brightness, fade_in=False, log_event=False)
        time.sleep(speed)
        led_off(fade_out=False, log_event=False)
        if i < times - 1:
            time.sleep(speed)
    
    if log_event:
        send_led_event("led_blinked", {"times": times, "speed": speed, "brightness": brightness})

def led_breathe(cycles=3, speed=2, log_event=True):
    """Breathe effect - fade in and out smoothly"""
    print(f"[LED] Breathing {cycles} cycles")
    
    for _ in range(cycles):
        for duty in range(0, 101, 2):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(speed / 100)
        for duty in range(100, -1, -2):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(speed / 100)
    
    if log_event:
        send_led_event("led_breathe_effect", {"cycles": cycles, "speed": speed})

def set_led_brightness(brightness, log_event=True):
    """Set LED to specific brightness (0-100)"""
    brightness = max(0, min(100, brightness))
    GPIO.output(LED_GND_PIN, GPIO.LOW)
    led_pwm.ChangeDutyCycle(brightness)
    print(f"[LED] Brightness set to: {brightness}%")
    
    if log_event:
        send_led_event("led_brightness_changed", {"brightness": brightness})

def led_cleanup():
    """Clean up GPIO resources"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    led_pwm.stop()
    GPIO.cleanup([LED_PIN, LED_GND_PIN])
    print("[LED] Cleanup completed")

# Test function with MQTT events
if __name__ == "__main__":
    try:
        print("Testing LED with MQTT events...")
        led_on(log_event=True)
        time.sleep(1)
        led_blink(times=2, speed=0.3, log_event=True)
        time.sleep(1)
        led_breathe(cycles=1, speed=2, log_event=True)
        time.sleep(1)
        led_off(log_event=True)
    finally:
        led_cleanup()