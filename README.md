# 🎖️ Casque Clone - Armure de Clone Trooper

> Projet d'armure complète de Clone Trooper de Star Wars avec HUD fonctionnel, analyse d'image par intelligence artificielle, et système de monitoring environnemental multi-capteurs.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture matérielle](#-architecture-matérielle)
- [Architecture logicielle](#-architecture-logicielle)
- [Structure du projet](#-structure-du-projet)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Documentation](#-documentation)
- [Roadmap](#-roadmap)

---

## 🎯 Vue d'ensemble

Ce projet vise à créer une armure fonctionnelle de Clone Trooper avec :

- **HUD binoculaire** : Affichage temps réel sur OLED transparent
- **Vision augmentée** : Détection d'objets par YOLO (IA)
- **Monitoring environnemental** : Température, humidité, qualité d'air, gaz dangereux
- **Système centralisé** : Communication MQTT entre tous les composants
- **Interface tactile** : Contrôle depuis le bras

---

## 🔧 Architecture matérielle

### **🪖 CASQUE**

| Composant | Description |
|-----------|-------------|
| **Pi Zero 2W (œil droit)** | Caméra Pi + OLED transparent 128x64 |
| **Pi Zero 2W (œil gauche)** | Caméra Pi + OLED transparent 128x64 |
| **ESP32-WROOM-32** | Gestion capteurs I2C + ventilation |

**Capteurs ESP32 casque :**
- GY-BNO055 : Orientation 9-DOF
- R287 : ENS160 (qualité air) + AHT21 (temp/humidité)
- GY-BME280 : Pression/température/humidité
- PCA9548A : Multiplexeur I2C
- INA219 : Monitoring batterie (optionnel)
- Ventilateur 5V 30x30mm

---

### **🎒 BACKPACK**

| Composant | Description |
|-----------|-------------|
| **Raspberry Pi 5** | Serveur central (WiFi AP + MQTT + YOLO) |
| **ESP32-WROOM-32** | Capteurs environnementaux multiples |

**Capteurs ESP32 backpack :**
- 2x R287 (ENS160+AHT21) : Intérieur + Extérieur
- 2x PCA9548A : Multiplexeurs I2C (int/ext)
- 2x GY-BME280 : Pression (int/ext)
- 2x MQ-2 : Détection fumée/gaz combustibles (int/ext)
- 2x MQ-7 : Détection CO (int/ext)
- INA219 : Monitoring batterie
- Ventilateur 5V 40x40mm

---

### **💪 BRAS**

| Composant | Description |
|-----------|-------------|
| **Pi Zero 2W** | Écran tactile de contrôle système |

---

### **🔋 ÉNERGIE**

| Composant | Description |
|-----------|-------------|
| **Pi Zero 2W** | Gestion pack batterie + monitoring |

---

## 🏛️ Architecture logicielle

### **Communication**
- **Protocole** : MQTT
- **Broker** : Mosquitto (Pi 5)
- **Réseau** : WiFi Access Point (Pi 5)

### **Stack technologique**
- **Langage principal** : Python 3.11+
- **Vision par ordinateur** : 
  - YOLO (Ultralytics)
  - OpenCV
  - PiCamera2
- **Affichage** : 
  - Luma.OLED (HUD)
  - Pygame/Kivy (tactile)
- **Hardware** : 
  - RPi.GPIO
  - smbus2 (I2C)
- **Embarqué** : 
  - MicroPython ou C++ (ESP32)

### **Topics MQTT** (standardisés)
Voir `shared/mqtt_topics.py` pour la liste complète.

---

## 📂 Structure du projet
```
Casqueclone/
│
├── helmet/                      # 🪖 Composants casque
│   ├── pi_zero_right_eye/       # HUD œil droit
│   ├── pi_zero_left_eye/        # HUD œil gauche
│   └── esp32_helmet/            # Capteurs casque
│
├── backpack/                    # 🎒 Serveur central
│   ├── pi5_server/              # MQTT + YOLO + WiFi AP
│   └── esp32_backpack/          # Capteurs environnementaux
│
├── arm/                         # 💪 Interface utilisateur
│   └── pi_zero_arm_display/     # Écran tactile contrôle
│
├── energy/                      # 🔋 Gestion énergie
│   └── pi_zero_energy/          # Monitoring batterie
│
├── shared/                      # 📦 Code partagé
│   ├── mqtt_topics.py           # Topics MQTT centralisés
│   ├── sensor_utils.py          # Utilitaires capteurs
│   ├── constants.py             # Constantes globales
│   └── logger.py                # Logging unifié
│
├── tests/                       # 🧪 Tests unitaires
│   ├── test_mqtt.py
│   ├── test_sensors.py
│   └── test_camera.py
│
├── docs/                        # 📖 Documentation
│   ├── wiring_diagrams/         # Schémas électriques
│   ├── 3d_models/               # Fichiers STL
│   ├── setup_guide.md           # Guide installation
│   └── mqtt_architecture.md     # Architecture MQTT
│
├── config/                      # ⚙️ Configurations
│   └── example.yaml             # Template config
│
├── .gitignore
├── README.md
└── requirements-dev.txt         # Dépendances développement
```

---

## 🚀 Installation

### **Prérequis**
- Python 3.11+
- Git
- Raspberry Pi OS (Bookworm) sur tous les Pi
- PlatformIO (pour ESP32)

### **1. Cloner le repository**
```bash
git clone https://github.com/Kypassart/Casqueclone.git
cd Casqueclone
```

### **2. Installation composant par composant**

**Exemple : HUD œil droit**
```bash
cd helmet/pi_zero_right_eye

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Installer dépendances
pip install -r requirements.txt

# Configurer
cp config.example.yaml config.yaml
# Éditer config.yaml avec tes paramètres
```

Répéter pour chaque composant.

---

## 🎮 Utilisation

### **Démarrage du système complet**

**1. Démarrer le serveur central (Backpack)**
```bash
ssh pi@pi-backpack.local
cd ~/Casqueclone/backpack/pi5_server
python main.py
```

**2. Démarrer les HUD**
```bash
# Œil droit
ssh pi@pi-right-eye.local
cd ~/Casqueclone/helmet/pi_zero_right_eye
python main.py

# Œil gauche
ssh pi@pi-left-eye.local
cd ~/Casqueclone/helmet/pi_zero_left_eye
python main.py
```

**3. Démarrer l'interface tactile**
```bash
ssh pi@pi-arm.local
cd ~/Casqueclone/arm/pi_zero_arm_display
python main.py
```

**Services systemd** disponibles pour auto-démarrage (voir docs/setup_guide.md).

---

## 📖 Documentation

- [📘 Guide d'installation complet](docs/setup_guide.md)
- [🔌 Schémas de câblage](docs/wiring_diagrams/)
- [🗺️ Architecture MQTT](docs/mqtt_architecture.md)
- [🧑‍💻 Guide développeur](docs/developer_guide.md)

---

## 🗓️ Roadmap

### Phase 1 : Infrastructure (En cours)
- [x] Structure projet
- [ ] Broker MQTT sur Pi 5
- [ ] WiFi Access Point
- [ ] Topics MQTT standardisés

### Phase 2 : Casque
- [ ] HUD basique (affichage texte)
- [ ] Capture caméra binoculaire
- [ ] Streaming MQTT des frames
- [ ] Capteurs ESP32 (BNO055, ENS160...)

### Phase 3 : IA & Vision
- [ ] YOLO sur Pi 5
- [ ] Détection objets temps réel
- [ ] Overlay HUD avec détections

### Phase 4 : Monitoring
- [ ] Dashboard backpack (temp, gaz, batterie)
- [ ] Alertes sécurité (CO, fumée)
- [ ] Interface tactile bras

### Phase 5 : Optimisation
- [ ] Latence <100ms camera→HUD
- [ ] Autonomie batterie optimisée
- [ ] Services systemd auto-start

---

## 👤 Auteur

**Kypassart**

---

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE) pour détails.

---

## 🙏 Remerciements

- Communauté 501st Legion
- Makers de la galaxie lointaine, très lointaine...

---

_"Good soldiers follow orders."_