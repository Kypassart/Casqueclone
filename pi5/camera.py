#!/usr/bin/env python3
import cv2
import subprocess

# --- Configuration ---
CAM_WIDTH = 640
CAM_HEIGHT = 480
FPS = 30

# --- Commande rpicam-vid pour capturer la caméra en MJPEG ---
# Sortie dans un pipe que OpenCV peut lire
cam_cmd = [
    "rpicam-vid",
    "-t", "0",  # temps infini
    "--inline",
    "--nopreview",
    "--width", str(CAM_WIDTH),
    "--height", str(CAM_HEIGHT),
    "--framerate", str(FPS),
    "--output", "-"  # sortie stdout
]

# --- Ouvrir le flux caméra via OpenCV ---
cam_process = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE, bufsize=10**8)

cap = cv2.VideoCapture(cam_process.stdout)

if not cap.isOpened():
    print("Impossible d'ouvrir la caméra")
    exit(1)

# --- Fenêtre fullscreen ---
cv2.namedWindow("Cam Fullscreen", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Cam Fullscreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Affiche l'image plein écran
    cv2.imshow("Cam Fullscreen", frame)

    # Quitte sur ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
