import paho.mqtt.client as mqtt
import time
import json

BROKER = "10.102.27.188"
PORT = 1883
TOPIC = "pillpal/device/events"
DEVICE_ID = "pi-zero-001"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id=DEVICE_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

try:
    while True:
        payload = {
            "device_id": DEVICE_ID,
            "event": "pill_taken",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        client.publish(TOPIC, json.dumps(payload))
        print(f"Sent event: {payload}")
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting…")
    client.disconnect()

