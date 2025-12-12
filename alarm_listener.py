import paho.mqtt.client as mqtt
from actuators.alerts import alert_start, alert_stop

DEVICE_ID = "1"
TOPIC = f"pillpal/device/{DEVICE_ID}/commands"

def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected. Subscribing...")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[MQTT] Received: {payload}")

    if payload == "ALERT_START":
        alert_start(sound=True, vibration=True, led=True)

    elif payload == "ALERT_STOP":
        alert_stop()

mqtt_client = mqtt.Client(client_id=f"listener-{DEVICE_ID}")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("localhost", 1883, 60)
print(f"Listening for alerts on {TOPIC}")
mqtt_client.loop_forever()
