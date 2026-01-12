# MQTT Topics – Casque Commando Clone

Ce document définit **l’ensemble des topics MQTT**, leurs payloads et leur rôle.
Il fait foi pour tous les développements (ESP32, Pi 5, Pi Zero).

---

## Broker MQTT

* Hébergé sur : **Raspberry Pi 5**
* Réseau local (AP Wi-Fi du Pi 5)
* QoS recommandé : **0 ou 1**

---

## ESP32 – Casque (Helmet)

### Environnement casque

**Topic** : `esp32/helmet/env`

```json
{
  "temp": 36.5,
  "humidity": 62
}
```

---

### Orientation / IMU

**Topic** : `esp32/helmet/imu`

```json
{
  "gx": 0.01,
  "gy": -0.02,
  "gz": 0.98,
  "heading": 270
}
```

---

### Ventilateur casque (commande)

**Topic** : `esp32/helmet/fan`

```json
{
  "state": "ON",
  "speed": 80
}
```

---

## ESP32 – Backpack

### Environnement interne

**Topic** : `esp32/backpack/env_internal`

```json
{
  "temp": 42.1,
  "humidity": 58
}
```

---

### Environnement externe

**Topic** : `esp32/backpack/env_external`

```json
{
  "temp": 30.4,
  "humidity": 71
}
```

---

### Qualité de l’air

**Topic** : `esp32/backpack/air`

```json
{
  "smoke": 0.02,
  "co2": 980
}
```

---

### Ventilateur backpack (commande)

**Topic** : `esp32/backpack/fan`

```json
{
  "state": "AUTO",
  "speed": 100
}
```

---

## Raspberry Pi Zero – Bras

### Commandes utilisateur

**Topic** : `pizero/controls`

```json
{
  "mode": "combat",
  "hud_brightness": 0.8,
  "confirm": true
}
```

---

### État Pi Zero

**Topic** : `pizero/status`

```json
{
  "battery": 74,
  "connected": true
}
```

---

## Raspberry Pi 5 – Statut système

### État global

**Topic** : `pi5/status`

```json
{
  "ai": "OK",
  "fps_left": 24,
  "fps_right": 23,
  "mqtt": "OK"
}
```

---

## Timeouts & Sécurité

| Source         | Timeout | Effet HUD          |
| -------------- | ------- | ------------------ |
| ESP32 casque   | 3 s     | Transparence tête  |
| ESP32 backpack | 3 s     | Transparence torse |
| Pi Zero        | 5 s     | Blocage commandes  |

---

## Règles générales

* Tous les payloads sont en JSON
* Pas de calcul critique côté ESP32
* Le Pi 5 est décisionnaire unique
* Toute donnée absente déclenche un mode dégradé HUD

---

## Notes

Ce document doit être mis à jour **avant toute modification des topics**.
