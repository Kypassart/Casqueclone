#!/usr/bin/env python3
import cv2
import time
from picamera2 import Picamera2

# --- INITIALISATION DES CAMERAS ---
cam_left = Picamera2(0)
cam_right = Picamera2(1)

config_left = cam_left.create_video_configuration(
    main={"size": (1920,1080), "format": "RGB888"}, buffer_count=6
)
config_right = cam_right.create_video_configuration(
    main={"size": (1920,1080), "format": "RGB888"}, buffer_count=6
)

cam_left.configure(config_left)
cam_right.configure(config_right)

cam_left.start()
cam_right.start()
time.sleep(1)  # laisse la caméra démarrer

# --- FENETRES PLEIN ECRAN SUR CHAQUE HDMI ---
cv2.namedWindow("LEFT", cv2.WINDOW_NORMAL)
cv2.moveWindow("LEFT", 0, 0)
cv2.setWindowProperty("LEFT", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.namedWindow("RIGHT", cv2.WINDOW_NORMAL)
cv2.moveWindow("RIGHT", 1920, 0)
cv2.setWindowProperty("RIGHT", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# --- BOUCLE D'AFFICHAGE ---
while True:
    frame_left = cam_left.capture_array()
    frame_right = cam_right.capture_array()

    cv2.imshow("LEFT", frame_left)
    cv2.imshow("RIGHT", frame_right)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC pour quitter
        break

cam_left.stop()
cam_right.stop()
cv2.destroyAllWindows()
