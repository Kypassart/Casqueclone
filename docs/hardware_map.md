# Hardware Map – Casque Commando Clone

## Vue d’ensemble

Ce document décrit la répartition physique et logique de tous les composants du système.

---

## Casque (tête)

### Composants

* Caméra CSI œil gauche
* Écran HDMI œil gauche
* Caméra CSI œil droit
* Écran HDMI œil droit
* Casque audio (écouteur + micro)
* ESP32 casque

### Capteurs ESP32 casque

* Température / humidité
* Gyroscope (X, Y, Z)
* Boussole (orientation absolue)
* Ventilateur (piloté)

### Rôle

* Fournir l’orientation du HUD
* Fournir l’état thermique interne du casque
* Commander le refroidissement du casque

---

## Dos de l’armure (Backpack)

### Composants

* Raspberry Pi 5 (cerveau central)
* SSD (OS + IA + HUD)
* Pack énergie
* ESP32 backpack
* Ventilateurs

### Capteurs ESP32 backpack

* Température / humidité intérieure
* Température / humidité extérieure
* Capteur fumée
* Capteur CO₂

### Rôle

* Traitement IA (détection de personnes)
* Fusion des données capteurs
* Génération du HUD
* Gestion thermique globale
* Sécurité environnementale

---

## Bras

### Composants

* Raspberry Pi Zero
* Écran tactile
* Batterie dédiée

### Rôle

* Interface utilisateur
* Commandes manuelles
* Sélection des modes HUD

---

## Communications

* Tous les modules communiquent via MQTT
* Le Raspberry Pi 5 agit comme broker et cerveau central

---

## Sorties visuelles

* HDMI gauche : œil gauche (caméra gauche + HUD)
* HDMI droit : œil droit (caméra droite + HUD)

---

## Notes

* L’architecture est pensée pour être modulaire et extensible
* Aucun traitement critique n’est effectué sur les ESP32 ou le Pi Zero
* Le Pi 5 est le point unique de décision
