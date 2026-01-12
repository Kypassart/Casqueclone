"""
camera.py
Gestion des deux caméras CSI (œil gauche / œil droit) via rpicam-vid
Sortie OpenCV compatible HUD
Pi OS Bookworm – Raspberry Pi 5
"""

import cv2
import subprocess
import threading

# Commandes rpicam pour chaque œil
PIPE_LEFT = (
    "rpicam-vid -t 0 --camera 0 --width 1280 --height 720 --framerate 30 "
    "--codec h264 --inline -o - | "
    "gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 "
    "! videoconvert ! appsink"
)

PIPE_RIGHT = (
    "rpicam-vid -t 0 --camera 1 --width 1280 --height 720 --framerate 30 "
    "--codec h264 --inline -o - | "
    "gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 "
    "! videoconvert ! appsink"
)

class CameraStream:
    def __init__(self, pipe, name="camera"):
        self.pipe = pipe
        self.name = name
        self.cap = None
        self.running = False
        self.frame = None

    def start(self):
        self.cap = cv2.VideoCapture(self.pipe, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise RuntimeError(f"Impossible d'ouvrir {self.name}")
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def read(self):
        return self.frame

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()


def start_dual_camera():
    left = CameraStream(PIPE_LEFT, "œil gauche")
    right = CameraStream(PIPE_RIGHT, "œil droit")

    left.start()
    right.start()

    return left, right


# Test standalone
if __name__ == "__main__":
    left, right = start_dual_camera()

    while True:
        if left.read() is not None:
            cv2.imshow("Oeil gauche", left.read())
        if right.read() is not None:
            cv2.imshow("Oeil droit", right.read())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    left.stop()
    right.stop()
    cv2.destroyAllWindows()
