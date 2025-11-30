# actuators/alerts.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

LED_PIN = 18
LED_GND_PIN = 15
BUZZER_PIN = 21
MOTOR_PIN = 12

# MQTT setup
BROKER = "localhost"
PORT = 1883
DEVICE_ID = "1"
TOPIC_EVENTS = "pillpal/device/events"

# Create MQTT client for alert events
mqtt_client = mqtt.Client(client_id=f"{DEVICE_ID}_alerts")
mqtt_client.connect(BROKER, PORT, keepalive=60)
mqtt_client.loop_start()

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_GND_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

led_pwm = GPIO.PWM(LED_PIN, 500)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
motor_pwm = GPIO.PWM(MOTOR_PIN, 200)

led_pwm.start(0)
buzzer_pwm.start(0)
motor_pwm.start(0)

NOTES = {
    "C5": 523,
    "E5": 659,
    "G5": 784,
    "R": 0
}

MELODY = [
    ("C5", 0.15), ("R", 0.05),
    ("E5", 0.15), ("G5", 0.15)
]

def send_alert_event(event_type, metadata=None):
    """Send alert event to MQTT and database"""
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
    print(f"[ALERT EVENT] {event_type}: {payload}")

def play_melody():
    """Play the melody and send event to database"""
    print("[ALERT] Playing melody")
    for note, duration in MELODY:
        freq = NOTES[note]
        if freq == 0:
            buzzer_pwm.ChangeDutyCycle(0)
        else:
            buzzer_pwm.ChangeFrequency(freq)
            buzzer_pwm.ChangeDutyCycle(60)
        time.sleep(duration)
    buzzer_pwm.ChangeDutyCycle(0)
    
    # Send melody event to database
    send_alert_event("melody_played", {"melody_type": "alert_tone"})

def turn_led(on=True, log_event=True):
    """Turn LED on/off with optional event logging"""
    if on:
        GPIO.output(LED_GND_PIN, GPIO.LOW)
        for duty in range(0, 101, 3):
            led_pwm.ChangeDutyCycle(duty)
            time.sleep(0.01)
        if log_event:
            send_alert_event("led_activated")
    else:
        led_pwm.ChangeDutyCycle(0)
        GPIO.output(LED_GND_PIN, GPIO.HIGH)
        if log_event:
            send_alert_event("led_deactivated")

def vibrate(on=True, log_event=True):
    """Turn vibration motor on/off with optional event logging"""
    if on:
        motor_pwm.ChangeDutyCycle(75)
        if log_event:
            send_alert_event("motor_activated", {"intensity": 75})
    else:
        motor_pwm.ChangeDutyCycle(0)
        if log_event:
            send_alert_event("motor_deactivated")

def alert_start(alert_type="standard"):
    """Start alert with all actuators and send event to database"""
    print(f"[ALERT] Starting {alert_type} alert")
    
    # Send alert start event to database
    send_alert_event("alert_started", {"alert_type": alert_type})
    
    # Original functionality
    turn_led(True, log_event=False)  # Don't log individual events for coordinated alert
    vibrate(True, log_event=False)   # Don't log individual events for coordinated alert
    
    if alert_type == "standard":
        buzzer_pwm.ChangeFrequency(800)
        buzzer_pwm.ChangeDutyCycle(50)
        send_alert_event("buzzer_activated", {"frequency": 800, "duty_cycle": 50})
    elif alert_type == "melody":
        play_melody()  # This will log its own event
    elif alert_type == "silent":
        # Silent alert - no buzzer
        send_alert_event("silent_alert_activated")
    elif alert_type == "vibration_only":
        # Vibration only alert
        send_alert_event("vibration_alert_activated")
    elif alert_type == "led_only":
        # LED only alert  
        send_alert_event("led_alert_activated")

def alert_stop():
    """Stop all alerts and send event to database"""
    print("[ALERT] Stopping all alerts")
    
    # Send alert stop event to database
    send_alert_event("alert_stopped")
    
    # Original functionality
    turn_led(False, log_event=False)  # Don't log individual events for coordinated stop
    vibrate(False, log_event=False)   # Don't log individual events for coordinated stop
    buzzer_pwm.ChangeDutyCycle(0)
    
    # Send individual deactivation events
    send_alert_event("buzzer_deactivated")

def alert_test():
    """Test all actuators with database logging"""
    print("[ALERT] Testing all actuators with MQTT events...")
    
    # Test LED with event logging
    turn_led(True)
    time.sleep(1)
    turn_led(False)
    time.sleep(0.5)
    
    # Test vibration with event logging
    vibrate(True)
    time.sleep(1)
    vibrate(False)
    time.sleep(0.5)
    
    # Test buzzer with event logging
    buzzer_pwm.ChangeFrequency(1000)
    buzzer_pwm.ChangeDutyCycle(50)
    send_alert_event("buzzer_activated", {"frequency": 1000, "duty_cycle": 50})
    time.sleep(1)
    buzzer_pwm.ChangeDutyCycle(0)
    send_alert_event("buzzer_deactivated")
    
    # Test melody
    play_melody()
    
    print("[ALERT] Test completed")

def individual_control():
    """Functions for individual actuator control with MQTT events"""
    
    def buzzer_on(frequency=800, duty_cycle=50):
        """Turn buzzer on individually with event logging"""
        buzzer_pwm.ChangeFrequency(frequency)
        buzzer_pwm.ChangeDutyCycle(duty_cycle)
        send_alert_event("buzzer_activated", {"frequency": frequency, "duty_cycle": duty_cycle})
    
    def buzzer_off():
        """Turn buzzer off individually with event logging"""
        buzzer_pwm.ChangeDutyCycle(0)
        send_alert_event("buzzer_deactivated")
    
    def motor_on(intensity=75):
        """Turn motor on individually with event logging"""
        motor_pwm.ChangeDutyCycle(intensity)
        send_alert_event("motor_activated", {"intensity": intensity})
    
    def motor_off():
        """Turn motor off individually with event logging"""
        motor_pwm.ChangeDutyCycle(0)
        send_alert_event("motor_deactivated")
    
    def led_on():
        """Turn LED on individually with event logging"""
        turn_led(True)
    
    def led_off():
        """Turn LED off individually with event logging"""
        turn_led(False)
    
    return buzzer_on, buzzer_off, motor_on, motor_off, led_on, led_off

# Create individual control functions
buzzer_on, buzzer_off, motor_on, motor_off, led_on, led_off = individual_control()

def cleanup():
    """Clean up all resources and send final event"""
    send_alert_event("device_cleanup")
    
    # Original cleanup functionality
    led_pwm.stop()
    buzzer_pwm.stop()
    motor_pwm.stop()
    
    # Stop MQTT client
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    
    GPIO.cleanup()
    print("[ALERT] Cleanup completed with MQTT events")

# Test function
if __name__ == "__main__":
    try:
        print("Testing alerts with MQTT database integration...")
        alert_test()
        time.sleep(1)
        
        print("Testing standard alert...")
        alert_start("standard")
        time.sleep(3)
        alert_stop()
        
        time.sleep(1)
        
        print("Testing melody alert...")
        alert_start("melody")
        time.sleep(2)
        alert_stop()
        
    finally:
        cleanup()