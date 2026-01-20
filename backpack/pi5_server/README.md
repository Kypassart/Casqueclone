# Backpack Pi 5 Server

Serveur central de l'armure - Gère le broker MQTT, l'analyse YOLO, et le WiFi Access Point.

## 🔧 Matériel

- Raspberry Pi 5 (4GB+ recommandé)
- Adaptateur WiFi compatible AP mode (intégré sur Pi 5)

## 📦 Installation
```bash
cd backpack/pi5_server

# Installer Mosquitto MQTT broker
sudo apt update
sudo apt install -y mosquitto mosquitto-clients

# Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configuration WiFi AP
sudo apt install -y hostapd dnsmasq
# Voir docs/setup_guide.md pour config complète
```

## 🚀 Utilisation
```bash
# Démarrer Mosquitto
sudo systemctl start mosquitto

# Démarrer le serveur Python
python main.py
```

## 📡 Architecture
```
┌─────────────────────────────────────┐
│         Raspberry Pi 5              │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ Mosquitto    │  │ YOLO Model  │ │
│  │ MQTT Broker  │  │ Detection   │ │
│  └──────────────┘  └─────────────┘ │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      WiFi Access Point       │  │
│  │   192.168.4.1/24             │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ├── Pi Zero (Right Eye)
         ├── Pi Zero (Left Eye)
         ├── Pi Zero (Arm Display)
         └── Pi Zero (Energy)
```

## 🧪 Tests
```bash
# Test MQTT
mosquitto_sub -h localhost -t '#' -v

# Test YOLO
python test_yolo.py
```
