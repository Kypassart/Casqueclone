# ESP32 Helmet - MicroPython

Gestion des capteurs du casque en **MicroPython**.

## 🔧 Matériel

- ESP32-WROOM-32
- Capteurs I2C :
  - BNO055 (orientation)
  - BME280 (temp/humidité/pression)
  - ENS160 + AHT21 (qualité air)
  - INA219 (batterie, optionnel)
  - PCA9548A (multiplexeur I2C)
- Ventilateur 5V 30x30mm

## 📦 Installation MicroPython

### 1. Télécharger MicroPython

https://micropython.org/download/esp32/

### 2. Flasher l'ESP32
```bash
# Effacer
esptool.py --port COM3 erase_flash

# Flasher
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 ESP32_GENERIC-XXXXXX.bin
```

### 3. Transférer les fichiers
```bash
# Installer mpremote
pip install mpremote

# Se connecter
mpremote connect COM3

# Copier les fichiers
mpremote fs cp config.py :config.py
mpremote fs cp boot.py :boot.py
mpremote fs cp sensors.py :sensors.py
mpremote fs cp mqtt_client.py :mqtt_client.py
mpremote fs cp main.py :main.py

# Redémarrer
mpremote reset
```

## 🚀 Utilisation
```bash
# Moniteur série
mpremote connect COM3

# Voir les logs
mpremote repl
```

## 📡 Topics MQTT publiés

- helmet/orientation : Données BNO055
- helmet/temp : Température
- helmet/humidity : Humidité
- helmet/pressure : Pression
- helmet/air_quality : Qualité de l'air
- helmet/power : Métriques batterie

## 🐛 Troubleshooting

**WiFi ne se connecte pas :**
```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()  # Voir les réseaux disponibles
```

**I2C ne détecte pas les capteurs :**
```python
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
i2c.scan()  # Liste les adresses I2C
```

**Erreur umqtt.simple :**
```bash
# Installer umqtt depuis mpremote
mpremote mip install umqtt.simple
```
