import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    def __init__(self, broker="localhost", port=1883, topic="pillpal/device/events", device_id="pi-zero"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.device_id = device_id
        self.client = mqtt.Client(client_id=device_id)

       
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(" Connected to MQTT broker")
            client.subscribe(self.topic)
        else:
            print(f" Failed connection → code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Message on {msg.topic}: {msg.payload.decode()}")

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)

    def publish_event(self, event_name):
        payload = {
            "device_id": self.device_id,
            "event": event_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.client.publish(self.topic, json.dumps(payload))
        print(f"Published: {payload}")

    def loop(self):
        self.client.loop_start()
