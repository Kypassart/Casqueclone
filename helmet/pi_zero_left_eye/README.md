# Helmet Left Eye - HUD System

Gère l'affichage HUD de l'œil droit et la capture vidéo pour analyse YOLO.

## ?? Matériel

- Raspberry Pi Zero 2W
- Camera Module v2 (ou compatible)
- OLED transparent 128x64 (SSD1306, I2C)

## ?? Installation
```bash
cd helmet/pi_zero_left_eye

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate
# Installer dépendances
pip install -r requirements.txt

# Configurer
cp config.yaml config.local.yaml
# Éditer config.local.yaml si nécessaire
```

## ?? Utilisation
```bash
python main.py
```

## ?? Topics MQTT

### Publie sur :
- helmet/left/frame : Frames caméra (JPEG compressé)
- helmet/left/temp : Température interne
- helmet/left/humidity : Humidité interne

### S'abonne à :
- ackpack/yolo/results : Résultats détection YOLO
- system/command : Commandes système

## ?? Troubleshooting

**Camera not detected:**
```bash
vcgencmd get_camera
# Should show: supported=1 detected=1
```
**I2C not working:**
```bash
sudo raspi-config
# Interface Options ? I2C ? Enable
sudo reboot

i2cdetect -y 1
# Should show 0x3C
```
**MQTT connection failed:**
- Vérifier que le Pi 5 (broker) est démarré
- Vérifier la connexion WiFi au AP
- Tester : ping 192.168.4.1
