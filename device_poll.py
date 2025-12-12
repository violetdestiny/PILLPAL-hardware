import requests
import time
from actuators.alerts import alert_start, alert_stop

DEVICE_ID = 7
BACKEND = "https://pillpal.space"

last_alert_state = False

def poll_backend():
    global last_alert_state

    while True:
        try:
            r = requests.get(f"{BACKEND}/api/device/poll?device_id={DEVICE_ID}", timeout=4)
            data = r.json()

            print("Received:", data)

            prefs = {
                "sound": data["sound"],
                "vibration": data["vibration"],
                "led": data["led"]
            }

            alert_flag = data.get("alert", False)

            if alert_flag and not last_alert_state:
                print(">>> STARTING ALARM!")
                alert_start(**prefs)

            if not alert_flag and last_alert_state:
                print(">>> STOPPING ALARM!")
                alert_stop()

            last_alert_state = alert_flag

        except Exception as e:
            print("Error polling backend:", e)

        time.sleep(5)


if __name__ == "__main__":
    poll_backend()
