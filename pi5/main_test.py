#!/usr/bin/env python3
import cv2
import time
import math
import random

from camera import CameraManager
from hud import draw_hud
from yolo_detect import YoloDetector

# ----------------------------
# INITIALISATION
# ----------------------------
camera_manager = CameraManager(width=1920, height=1080)
yolo = YoloDetector(model_path='yolov8n.pt')  # adapte si modèle local

# --- HUD dynamique (simulation) ---
hud_data = {
    "orientation": 0,
    "battery_level": 4,
    "casque_temp": 25,
    "casque_humidity": 50,
    "temp_ext": 25,
    "humidity_ext": 50,
    "backpack_temp": 25,
    "backpack_humidity": 50,
    "air_quality_ext": 0,
    "air_quality_int": 0,
    "target_found": False,
    "lost_connection": False
}

# Variables pour test dynamique
battery_dir = 1
orientation_dir = 1
temp_dir = 1

# ----------------------------
# BOUCLE PRINCIPALE
# ----------------------------
try:
    while True:
        # --- Récupération frames ---
        frame_left, frame_right = camera_manager.get_frames()

        # --- Simulation données dynamiques HUD ---
        hud_data["battery_level"] += battery_dir * 0.01
        if hud_data["battery_level"] >= 4:
            hud_data["battery_level"] = 4
            battery_dir = -1
        elif hud_data["battery_level"] <= 0:
            hud_data["battery_level"] = 0
            battery_dir = 1

        hud_data["orientation"] = (hud_data["orientation"] + orientation_dir*0.5) % 360
        if random.random() < 0.01:
            orientation_dir *= -1

        hud_data["casque_temp"] += temp_dir * 0.05
        hud_data["backpack_temp"] += temp_dir * 0.05
        hud_data["temp_ext"] += temp_dir * 0.03
        if hud_data["casque_temp"] > 50 or hud_data["casque_temp"] < 20:
            temp_dir *= -1

        hud_data["casque_humidity"] = 50 + 30*math.sin(time.time()/5)
        hud_data["humidity_ext"] = 50 + 30*math.cos(time.time()/6)

        hud_data["air_quality_ext"] = int((math.sin(time.time()/10)+1)*1.5)  # 0,1,2
        hud_data["air_quality_int"] = int((math.cos(time.time()/8)+1)*1.5)

        hud_data["target_found"] = random.random() < 0.01
        hud_data["lost_connection"] = random.random() < 0.005

        # --- YOLO sur oeil gauche ---
        frame_left = yolo.detect(frame_left)

        # --- Dessin HUD sur les deux yeux ---
        frame_left = draw_hud(frame_left, hud_data)
        frame_right = draw_hud(frame_right, hud_data)

        # --- Affichage ---
        cv2.imshow("LEFT", frame_left)
        cv2.imshow("RIGHT", frame_right)

        # Quitter avec ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    camera_manager.stop()
    cv2.destroyAllWindows()
