# **PillPal — Hardware (IoT Smart Pillbox)**

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Zero%202W-C51A4A?style=for-the-badge\&logo=raspberrypi\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-660066?style=for-the-badge\&logo=mqtt\&logoColor=white)
![GPIO](https://img.shields.io/badge/GPIO-FFCC00?style=for-the-badge)
![PiSugar](https://img.shields.io/badge/PiSugar-Battery%20Module-blue?style=for-the-badge)
![3D Printing](https://img.shields.io/badge/3D--Printed-Enclosure-orange?style=for-the-badge)


| Component                     | Link                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Frontend (Android)**        | [https://github.com/f4eriebambi/pillpalMobile](https://github.com/f4eriebambi/pillpalMobile |
| **Backend (Node.js + MySQL)** | [https://github.com/violetdestiny/PILLPAL-Backend](https://github.com/violetdestiny/PILLPAL-Backend)   |

---

## Authors

Team **Pixel Health**

* Sofia — Hardware + Backend
* Iker — Hardware + Connectivity
* Favour — UI/UX
* Ikram — Frontend + Integration

---

## **Overview**

The PillPal hardware is a **portable smart pillbox**, built using a Raspberry Pi Zero and a set of sensors/actuators that allow it to:

* Detect when the lid is opened (via **reed switch**)
* Alert users via **vibration motor**, **buzzer**, and **LED indicator**
* Publish medication events to the backend via **MQTT**
* Receive schedule updates from the backend (future support)
* Operate on-the-go using a **PiSugar battery module**

The device is approximately the size of an **AirPods case**, making it easy to carry on a lanyard, bag, or in a pocket.

---

##  **System Architecture**

<img width="614" height="509" alt="SysArchitecture" src="https://github.com/user-attachments/assets/33c0dcf1-a3c3-42f3-879e-f7ddcf0692ba" />

---

## **Components Used**

| Component                    | Purpose                |
| ---------------------------- | ---------------------- |
| **Raspberry Pi Zero**        | Main processor + WiFi  |
| **Reed Switch**              | Detects lid open/close |
| **Neodymium Magnet**         | Triggers reed switch   |
| **Vibration Motor (3V)**     | Tactile alert          |
| **Piezo Buzzer**             | Audible alert          |
| **LED Indicator**            | Visual alert           |
| **PiSugar 2 Battery Module** | Portable power supply  |
| **3D-printed enclosure**     | Housing + hinge system |

---

## **MQTT Event Structure**

The device publishes to:

```
pillpal/device/<device_id>
```

### Example Payload: `alert_started`

```json
{
  "device_id": "PILLPAL-01",
  "event": "alert_started",
  "timestamp": "2025-10-12T08:00:00Z"
}
```

### Example Payload: `pill_taken`

```json
{
  "device_id": "PILLPAL-01",
  "event": "pill_taken",
  "timestamp": "2025-10-12T08:03:12Z"
}
```

---

## **GPIO Pin Mapping**

| Component                 | GPIO Pin                                    |
| ------------------------- | ------------------------------------------- |
| Reed Switch               | GPIO 17                                     |
| Buzzer                    | GPIO 22                                     |
| Vibration Motor           | GPIO 27 (via transistor/MOSFET recommended) |
| LED Indicator             | GPIO 23                                     |
| Status LED (optional)     | GPIO 24                                     |
| PiSugar Battery Telemetry | I2C (SCL 3, SDA 2)                          |

> TO BE UPDATED!

---

## **Firmware Overview (Python)**

Your typical device loop:

```
1. Read lid state from reed switch
2. If lid opens → publish "pill_taken"
3. Listen for scheduled alerts (future)
4. Trigger:
   - Vibration motor
   - Buzzer
   - LED flash
5. Publish "alert_started" when reminder time arrives
6. Send battery info (optional)
```

---

## **Setup & Installation**

### 1. Install dependencies on the Pi

```bash
sudo apt update
sudo apt install python3-pip
pip3 install paho-mqtt RPi.GPIO
```

### 2️. Clone the repository

```bash
git clone https://github.com/violetdestiny/PILLPAL-Hardware
```

### 3️. Run the firmware

```bash
python3 main.py
```

### 4. Configure MQTT Broker

Use Mosquitto or your backend server’s broker.

