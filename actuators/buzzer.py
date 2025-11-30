# actuators/buzzer.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

BUZZER_PIN = 21

# MQTT setup
BROKER = "localhost"
PORT = 1883
DEVICE_ID = "1"
TOPIC_EVENTS = "pillpal/device/events"

# Create MQTT client for buzzer events
mqtt_client = mqtt.Client(client_id=f"{DEVICE_ID}_buzzer")
mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
buzzer_pwm.start(0)

# Musical notes for different alert types
NOTES = {
    "alert": 800,
    "warning": 600,
    "confirm": 1000,
    "error": 400
}

def send_buzzer_event(event_type, metadata=None):
    """Send buzzer event to MQTT and database"""
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
    print(f"[BUZZER EVENT] {event_type}: {payload}")

def buzzer_on(frequency=800, duty_cycle=50, log_event=True):
    """Turn buzzer on with specific frequency"""
    buzzer_pwm.ChangeFrequency(frequency)
    buzzer_pwm.ChangeDutyCycle(duty_cycle)
    print(f"[BUZZER] ON - freq: {frequency}Hz, duty: {duty_cycle}%")
    
    if log_event:
        send_buzzer_event("buzzer_activated", {"frequency": frequency, "duty_cycle": duty_cycle})

def buzzer_off(log_event=True):
    """Turn buzzer off"""
    buzzer_pwm.ChangeDutyCycle(0)
    print("[BUZZER] OFF")
    
    if log_event:
        send_buzzer_event("buzzer_deactivated")

def play_melody(melody_type="alert", log_event=True):
    """Play different melodies based on alert type"""
    print(f"[BUZZER] Playing melody: {melody_type}")
    
    if melody_type == "alert":
        melody = [(800, 0.3), (0, 0.1), (800, 0.3), (0, 0.1), (800, 0.3)]
    elif melody_type == "warning":
        melody = [(600, 0.2), (700, 0.2), (600, 0.2)]
    elif melody_type == "confirm":
        melody = [(1000, 0.1), (1200, 0.1), (1000, 0.1)]
    elif melody_type == "error":
        melody = [(400, 0.5), (300, 0.5)]
    else:
        melody = [(800, 0.5)]
    
    for freq, duration in melody:
        if freq > 0:
            buzzer_pwm.ChangeFrequency(freq)
            buzzer_pwm.ChangeDutyCycle(60)
        else:
            buzzer_pwm.ChangeDutyCycle(0)
        time.sleep(duration)
    
    buzzer_pwm.ChangeDutyCycle(0)
    
    if log_event:
        send_buzzer_event("buzzer_melody_played", {"melody_type": melody_type})

def buzzer_beep(times=1, duration=0.1, frequency=1000, log_event=True):
    """Simple beep pattern"""
    print(f"[BUZZER] Beeping {times} times")
    
    for i in range(times):
        buzzer_on(frequency, log_event=False)
        time.sleep(duration)
        buzzer_off(log_event=False)
        if i < times - 1:
            time.sleep(0.1)
    
    if log_event:
        send_buzzer_event("buzzer_beep_pattern", {"times": times, "duration": duration, "frequency": frequency})

def buzzer_cleanup():
    """Clean up GPIO resources"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    buzzer_pwm.stop()
    GPIO.cleanup(BUZZER_PIN)
    print("[BUZZER] Cleanup completed")

# Test function with MQTT events
if __name__ == "__main__":
    try:
        print("Testing buzzer with MQTT events...")
        buzzer_on(log_event=True)
        time.sleep(1)
        buzzer_off(log_event=True)
        time.sleep(1)
        play_melody("confirm", log_event=True)
        time.sleep(1)
        buzzer_beep(times=3, log_event=True)
    finally:
        buzzer_cleanup()