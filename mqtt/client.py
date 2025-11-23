import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import paho.mqtt.client as mqtt
import json
import requests
from datetime import datetime, timezone
import RPi.GPIO as GPIO

from sensors.lid import detect_lid_events
from actuators.alerts import alert_start, alert_stop

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "1"

TOPIC_EVENTS = "pillpal/device/events"
TOPIC_COMMANDS = "pillpal/device/commands"

API_URL = "https://pillpal.space/api/events"

mqtt_client = mqtt.Client(client_id=DEVICE_ID)


def send_event(event_type):
    payload = {
        "device_id": DEVICE_ID,
        "event_type": event_type,
        "source": "device",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    mqtt_client.publish(TOPIC_EVENTS, json.dumps(payload), qos=1)
    print(f"[MQTT] Published {payload}")

    try:
        res = requests.post(
            API_URL,
            json=payload,
            timeout=2
        )
        print(f"[HTTP] POST {res.status_code} {res.text}")
    except Exception as e:
        print(f"[HTTP ERROR] {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected to broker")
        client.subscribe(TOPIC_COMMANDS)
    else:
        print(f"[MQTT ERROR] Connection failed: {rc}")


def on_message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(f"[CMD] {cmd}")

    if cmd == "ALERT_START":
        alert_start()
    elif cmd == "ALERT_STOP":
        alert_stop()


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

print("Listening for lid events...")

try:
    detect_lid_events(
        lambda: send_event("lid_opened"),
        lambda: send_event("lid_closed")
    )
except KeyboardInterrupt:
    print("Stopping...")
finally:
    mqtt_client.loop_stop()
    GPIO.cleanup()
