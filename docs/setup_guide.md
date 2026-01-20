# 📘 Guide d'installation Casqueclone

Guide complet pour configurer l'ensemble du système.

## 🎯 Vue d'ensemble

Installation en 5 étapes :
1. Préparation hardware
2. Installation OS sur tous les Pi
3. Configuration réseau et MQTT
4. Déploiement du code
5. Tests et validation

---

## 1️⃣ Préparation Hardware

### Matériel nécessaire

**Casque :**
- 2x Raspberry Pi Zero 2W
- 2x Camera Module v2
- 2x OLED transparent 128x64 (I2C)
- 1x ESP32-WROOM-32
- Capteurs : BNO055, ENS160, AHT21, BME280, INA219
- Ventilateur 5V 30x30mm

**Backpack :**
- 1x Raspberry Pi 5 (4GB+)
- 1x ESP32-WROOM-32
- Capteurs multiples (voir README principal)
- Ventilateur 5V 40x40mm

**Bras :**
- 1x Raspberry Pi Zero 2W
- 1x Écran tactile

**Énergie :**
- 1x Raspberry Pi Zero 2W
- Pack batterie
- INA219

### Câblage I2C

*TODO: Ajouter schémas de câblage*

---

## 2️⃣ Installation Raspberry Pi OS

### Sur TOUS les Pi
```bash
# Utiliser Raspberry Pi Imager
# OS: Raspberry Pi OS Lite (64-bit) - Bookworm
# Configurer :
# - Hostname (pi-right-eye, pi-left-eye, pi-backpack, pi-arm, pi-energy)
# - Enable SSH
# - Username: pi
# - Password: <votre_mot_de_passe>
# - WiFi (temporaire, pour setup initial)
```

### Première connexion
```bash
ssh pi@pi-right-eye.local
sudo apt update && sudo apt upgrade -y
sudo raspi-config
# Interface Options → Enable I2C, Camera
sudo reboot
```

---

## 3️⃣ Configuration Pi 5 - Serveur central

### A. WiFi Access Point
```bash
sudo apt install -y hostapd dnsmasq

# Stopper services
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Configuration dhcpcd
sudo nano /etc/dhcpcd.conf
# Ajouter :
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant

# Configuration dnsmasq
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
# Ajouter :
interface=wlan0
dhcp-range=192.168.4.10,192.168.4.50,255.255.255.0,24h

# Configuration hostapd
sudo nano /etc/hostapd/hostapd.conf
# Ajouter :
interface=wlan0
driver=nl80211
ssid=CloneTrooper-HUD
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=Order66Execute
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# Lier la config
sudo nano /etc/default/hostapd
# Modifier :
DAEMON_CONF="/etc/hostapd/hostapd.conf"

# Activer le forwarding
sudo nano /etc/sysctl.conf
# Décommenter :
net.ipv4.ip_forward=1

# Démarrer
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```

### B. MQTT Broker
```bash
sudo apt install -y mosquitto mosquitto-clients

# Configuration
sudo nano /etc/mosquitto/mosquitto.conf
# Ajouter :
listener 1883
allow_anonymous true

sudo systemctl restart mosquitto
sudo systemctl enable mosquitto

# Test
mosquitto_sub -h localhost -t '#' -v
```

---

## 4️⃣ Déploiement du code

### Sur chaque Pi
```bash
# Cloner le repo
cd ~
git clone https://github.com/Kypassart/Casqueclone.git
cd Casqueclone

# Exemple : Pi Zero Right Eye
cd helmet/pi_zero_right_eye
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copier et éditer config
cp config.yaml config.local.yaml
nano config.local.yaml

# Test
python main.py
```

---

## 5️⃣ Services systemd (auto-démarrage)

### Exemple : Right Eye
```bash
sudo nano /etc/systemd/system/helmet-right.service
```
```ini
[Unit]
Description=Helmet Right Eye HUD
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Casqueclone/helmet/pi_zero_right_eye
ExecStart=/home/pi/Casqueclone/helmet/pi_zero_right_eye/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable helmet-right.service
sudo systemctl start helmet-right.service
sudo systemctl status helmet-right.service
```

Répéter pour tous les composants.

---

## ✅ Tests de validation
```bash
# Test WiFi AP
# Depuis un PC/téléphone, connecter au WiFi "CloneTrooper-HUD"

# Test MQTT
mosquitto_sub -h 192.168.4.1 -t '#' -v

# Test caméras
libcamera-hello

# Test I2C
i2cdetect -y 1
```

---

## 🐛 Troubleshooting

Voir fichiers README de chaque composant.
