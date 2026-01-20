# ESP32 Backpack - MicroPython

Surveillance environnementale complète du backpack.

## 🔧 Capteurs

**I2C (via multiplexeurs) :**
- 2x BME280 (int/ext)
- 2x ENS160 + AHT21 (int/ext)
- INA219 (batterie)
- 2x PCA9548A (multiplexeurs)

**Analogiques :**
- 2x MQ-2 (fumée/gaz int/ext)
- 2x MQ-7 (CO int/ext)

## 📡 Topics MQTT

- ackpack/temp/interior
- ackpack/temp/exterior
- ackpack/air_quality/interior
- ackpack/air_quality/exterior
- ackpack/gas/smoke/interior
- ackpack/gas/smoke/exterior
- ackpack/gas/co/interior
- ackpack/gas/co/exterior
- system/alerts (alertes dangers)

## ⚠️ Alertes

Le système publie des alertes sur system/alerts si :
- CO > 50 ppm (intérieur)
- Fumée > 300 ppm (intérieur)
