# 🪖 Clone Trooper AR Helmet

Casque de réalité augmentée inspiré des Clone Troopers de Star Wars avec détection IA temps réel.

## 🎯 Fonctionnalités

- 🎥 Vision binoculaire (2 caméras)
- 🤖 Détection IA personnes + armes (YOLOv8)
- 📊 HUD temps réel sur OLED transparent
- 🧭 Boussole et capteurs environnementaux
- 🔌 Déconnexion rapide magnétique (1 seconde)

## 📦 Matériel

- 2x Raspberry Pi Zero 2W
- 2x Raspberry Pi 5
- 2x Caméra Pi Module 3
- 2x OLED SSD1309 128x64 transparent
- 4x ESP32
- Capteurs (DHT22, BNO055, etc.)

## 🚀 Quick Start
```bash
# Installation Pi Zero
cd scripts/setup
./install_pi_zero.sh

# Installation Pi5
./install_pi5.sh

# Lancer système
cd src/pi_zero
python3 hud_display.py
```

## 📚 Documentation

Voir dossier `docs/` pour documentation complète.