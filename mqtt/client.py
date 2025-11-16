import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone
import RPi.GPIO as GPIO
from sensors.lid import detect_lid_open
from actuators.alerts import alert_start, alert_stop

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "pi-zero-pillpal-001"

TOPIC_EVENTS = "pillpal/device/events"
TOPIC_COMMANDS = "pillpal/device/commands"

mqtt_client = mqtt.Client(client_id=DEVICE_ID)

def send_event(event_type):
    payload = {
        "device_id": DEVICE_ID,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    mqtt_client.publish(TOPIC_EVENTS, json.dumps(payload), qos=1)
    print(f"[EVENT] Published: {payload}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC_COMMANDS)
    else:
        print(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(f"[CMD] {cmd}")

    if cmd == "ALERT_START":
        alert_start(sound=True, vibration=True)
    elif cmd == "ALERT_STOP":
        alert_stop()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

try:
    detect_lid_open(lambda: send_event("lid_opened"))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    mqtt_client.loop_stop()
    GPIO.cleanup()
