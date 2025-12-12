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

# -----------------------------
# CONFIG
# -----------------------------
BROKER = "localhost"        # MQTT interno (funciona en hotspot)
PORT = 1883

DEVICE_ID = "1"

TOPIC_EVENTS = "pillpal/device/events"
TOPIC_COMMANDS = "pillpal/device/commands"

# Endpoint de backend — si falla no rompe la demo
API_URL = "https://pillpal.space/api/events"

# Estado local de preferencias
user_pref_sound = True
user_pref_vibration = True
user_pref_led = True

# MQTT client
mqtt_client = mqtt.Client(client_id=f"device_{DEVICE_ID}")


# -----------------------------
# UTIL: enviar evento a MQTT + backend
# -----------------------------
def send_event(event_type):
    """Envía un evento desde el dispositivo al broker MQTT y al backend."""
    payload = {
        "device_id": DEVICE_ID,
        "event_type": event_type,
        "source": "device",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # --- MQTT publish (siempre funciona) ---
    mqtt_client.publish(TOPIC_EVENTS, json.dumps(payload), qos=1)
    print(f"[MQTT → BROKER] Published {payload}")

    # --- HTTP to backend (no afecta si falla) ---
#    try:
 #       res = requests.post(API_URL, json=payload, timeout=2)
  #      print(f"[HTTP] POST {res.status_code} {res.text}")
   # except Exception as e:
    #    print(f"[HTTP ERROR] {e} (demo continues normally)")


# -----------------------------
# CALLBACKS
# -----------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected → Subscribing to commands...")
        client.subscribe(TOPIC_COMMANDS)
    else:
        print(f"[MQTT] Failed connect: {rc}")


def on_message(client, userdata, msg):
    global user_pref_sound, user_pref_vibration, user_pref_led

    cmd = msg.payload.decode()
    print(f"[MQTT] Received command: {cmd}")

    if cmd == "ALERT_START":
        alert_start(user_pref_sound, user_pref_vibration, user_pref_led)

    elif cmd == "ALERT_STOP":
        alert_stop()

    elif cmd == "SET_PREF_SOUND_ON":
        user_pref_sound = True
    elif cmd == "SET_PREF_SOUND_OFF":
        user_pref_sound = False

    elif cmd == "SET_PREF_VIB_ON":
        user_pref_vibration = True
    elif cmd == "SET_PREF_VIB_OFF":
        user_pref_vibration = False

    elif cmd == "SET_PREF_LED_ON":
        user_pref_led = True
    elif cmd == "SET_PREF_LED_OFF":
        user_pref_led = False


# -----------------------------
# MQTT INIT
# -----------------------------
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("[MQTT] Connecting to broker...")
mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()


# -----------------------------
# MAIN PROGRAM (sensor loop)
# -----------------------------
try:
    print("Device running. Listening for lid events...")
    
    detect_lid_events(
        on_open=lambda: send_event("lid_opened"),
        on_close=lambda: send_event("lid_closed")
    )

except KeyboardInterrupt:
    print("KeyboardInterrupt received → Exiting gracefully")

finally:
    print("Stopping MQTT loop & cleaning GPIO...")
    mqtt_client.loop_stop()
    GPIO.cleanup()
