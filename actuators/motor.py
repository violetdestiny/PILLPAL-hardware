# actuators/motor.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

MOTOR_PIN = 12

# MQTT setup
BROKER = "localhost"
PORT = 1883
DEVICE_ID = "1"
TOPIC_EVENTS = "pillpal/device/events"

# Create MQTT client for motor events
mqtt_client = mqtt.Client(client_id=f"{DEVICE_ID}_motor")
mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

motor_pwm = GPIO.PWM(MOTOR_PIN, 200)
motor_pwm.start(0)

def send_motor_event(event_type, metadata=None):
    """Send motor event to MQTT and database"""
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
    print(f"[MOTOR EVENT] {event_type}: {payload}")

def motor_on(intensity=75, log_event=True):
    """Turn vibration motor on with specified intensity"""
    intensity = max(0, min(100, intensity))
    motor_pwm.ChangeDutyCycle(intensity)
    print(f"[MOTOR] ON - intensity: {intensity}%")
    
    if log_event:
        send_motor_event("motor_activated", {"intensity": intensity})

def motor_off(log_event=True):
    """Turn vibration motor off"""
    motor_pwm.ChangeDutyCycle(0)
    print("[MOTOR] OFF")
    
    if log_event:
        send_motor_event("motor_deactivated")

def motor_pulse(times=3, duration=0.5, intensity=75, log_event=True):
    """Pulse motor vibration specified number of times"""
    print(f"[MOTOR] Pulsing {times} times")
    
    for i in range(times):
        motor_on(intensity, log_event=False)
        time.sleep(duration)
        motor_off(log_event=False)
        if i < times - 1:
            time.sleep(0.2)
    
    if log_event:
        send_motor_event("motor_pulsed", {"times": times, "duration": duration, "intensity": intensity})

def motor_pattern(pattern_type="alert", log_event=True):
    """Play different vibration patterns"""
    print(f"[MOTOR] Playing pattern: {pattern_type}")
    
    if pattern_type == "alert":
        motor_pulse(times=3, duration=0.3, intensity=80, log_event=False)
    elif pattern_type == "notification":
        motor_pulse(times=2, duration=0.1, intensity=50, log_event=False)
    elif pattern_type == "warning":
        motor_on(60, log_event=False)
        time.sleep(1)
        motor_off(log_event=False)
    elif pattern_type == "confirm":
        motor_pulse(times=1, duration=0.1, intensity=40, log_event=False)
    
    if log_event:
        send_motor_event("motor_pattern_played", {"pattern_type": pattern_type})

def set_motor_intensity(intensity, log_event=True):
    """Set motor vibration intensity (0-100)"""
    intensity = max(0, min(100, intensity))
    motor_pwm.ChangeDutyCycle(intensity)
    print(f"[MOTOR] Intensity set to: {intensity}%")
    
    if log_event:
        send_motor_event("motor_intensity_changed", {"intensity": intensity})

def motor_cleanup():
    """Clean up GPIO resources"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    motor_pwm.stop()
    GPIO.cleanup(MOTOR_PIN)
    print("[MOTOR] Cleanup completed")

# Test function with MQTT events
if __name__ == "__main__":
    try:
        print("Testing motor with MQTT events...")
        motor_on(log_event=True)
        time.sleep(1)
        motor_off(log_event=True)
        time.sleep(1)
        motor_pulse(log_event=True)
        time.sleep(1)
        motor_pattern("alert", log_event=True)
    finally:
        motor_cleanup()