from pillpal_device.mqtt_client import MQTTClient
from pillpal_device.hardware import Hardware
import time

mqtt = MQTTClient(broker="localhost", device_id="pi-zero-001")
hw = Hardware()

def main():
    mqtt.connect()
    mqtt.loop()

    print(" PillPal device running...")

    last_state = None

    try:
        while True:
            is_open = hw.reed_is_open()

            if is_open != last_state:
                if is_open:
                    mqtt.publish_event("lid_opened")
                else:
                    mqtt.publish_event("lid_closed")

                last_state = is_open

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
        hw.cleanup()

if __name__ == "__main__":
    main()
