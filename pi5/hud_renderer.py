import cv2
import numpy as np
import math

# ----------------------------
# VARIABLES HUD DYNAMIQUES
# ----------------------------
hud_data = {
    "orientation": 0,          # 0° = nord
    "battery_level": 4,        # 0 à 4
    "casque_temp": 25,
    "casque_humidity": 50,
    "temp_ext": 25,
    "humidity_ext": 50,
    "backpack_temp": 25,
    "backpack_humidity": 50,
    "air_quality_ext": 0,      # 0=vert,1=orange,2=rouge
    "air_quality_int": 0,
    "target_found": False,
    "lost_connection": False
}

# ----------------------------
# UTILITAIRES COULEUR
# ----------------------------
def color_gradient(val, vmin, vmax, start_color, end_color):
    """Retourne une couleur RGB entre start_color et end_color en fonction de val"""
    ratio = max(0,min(1,(val-vmin)/(vmax-vmin)))
    return tuple(int(s*(1-ratio)+e*ratio) for s,e in zip(start_color,end_color))

# ----------------------------
# FONCTION BOUSSOLE LINÉAIRE
# ----------------------------
def draw_compass(frame, orientation, thickness=3):
    """
    Dessine une boussole style peigne en haut de l'écran.
    - Traits tous les degrés
    - Traits plus grands tous les 5°
    - Traits encore plus grands tous les 10° avec chiffre
    - Lettres N/E/S/O si visibles
    - Épaisseur identique au cube du casque
    - 120° centrés sur l'orientation du casque
    """
    h, w, _ = frame.shape
    compass_width = w - 100  # marge de 50px de chaque côté
    top_y = 50
    center_x = w // 2
    visible_deg = 120
    deg_per_pixel = visible_deg / compass_width

    for px in range(compass_width):
        deg = orientation - visible_deg/2 + px * deg_per_pixel
        deg_mod = int(deg) % 360

        # Définir hauteur du trait selon l'intervalle
        if deg_mod % 10 == 0:
            line_height = 25  # grand trait
            cv2.line(frame, (px+50, top_y), (px+50, top_y+line_height), (0,255,0), thickness)
            text = f"{deg_mod}°"
            cv2.putText(frame, text, (px-10+50, top_y + line_height + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 1)
        elif deg_mod % 5 == 0:
            line_height = 15  # moyen
            cv2.line(frame, (px+50, top_y), (px+50, top_y+line_height), (0,255,0), thickness)
        else:
            line_height = 8   # petit
            cv2.line(frame, (px+50, top_y), (px+50, top_y+line_height), (0,255,0), thickness)

    # Lettres cardinales
    cardinals = {"N":0, "E":90, "S":180, "O":270}
    for label, deg_card in cardinals.items():
        delta_deg = (deg_card - orientation + 180) % 360 - 180
        if abs(delta_deg) <= visible_deg/2:
            x = int(center_x + (delta_deg / (visible_deg/2)) * (compass_width/2))
            cv2.putText(frame, label, (x-10, top_y + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), thickness)
# ----------------------------
# FONCTION HUD
# ----------------------------
def draw_hud(frame, data=hud_data):
    h, w, _ = frame.shape
    center = (w//2, h//2)

    # --- POINT CENTRAL AVEC PETITE CROIX ---
    point_size = 5
    cross_size = 10
    cv2.circle(frame, center, point_size, (0,255,0), -1)
    # croix
    cv2.line(frame, (center[0]-cross_size//2, center[1]), (center[0]+cross_size//2, center[1]), (0,255,0), 2)
    cv2.line(frame, (center[0], center[1]-cross_size//2), (center[0], center[1]+cross_size//2), (0,255,0), 2)

    # --- CADRE AUTOUR DU POINT (100x100) ---
    box_size = 100
    color_box = (0,255,0) if data["target_found"] else (0,0,255)
    top_left = (center[0]-box_size//2, center[1]-box_size//2)
    bottom_right = (center[0]+box_size//2, center[1]+box_size//2)
    cv2.rectangle(frame, top_left, bottom_right, color_box, 2)

    # --- Boussole ---
    draw_compass(frame, data["orientation"])

    # --- BATTERIE HORIZONTALE BAS GAUCHE ---
    battery_x, battery_y = 50, h-80
    battery_w, battery_h = 30, 50
    spacing = 10
    total_width = 4*battery_w + 3*spacing
    cv2.rectangle(frame,
                  (battery_x-5, battery_y-30),
                  (battery_x + total_width + 5, battery_y + battery_h + 5),
                  (255,255,255), 2)
    cv2.putText(frame, "BATTERIE", (battery_x, battery_y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    for i in range(4):
        color = (0,255,0) if i < data["battery_level"] else (50,50,50)
        rect_top_left = (battery_x + i*(battery_w+spacing), battery_y)
        rect_bottom_right = (rect_top_left[0]+battery_w, battery_y+battery_h)
        cv2.rectangle(frame, rect_top_left, rect_bottom_right, color, -1)

    # --- ARMURE COIN BAS DROIT ---
    overlay = frame.copy()
    alpha = 0.5 if data["lost_connection"] else 1.0
    margin = 50
    arm_center = (w - 150 - margin, h - 250 - margin)
    arm_width, arm_height = 100, 200

    # Ovale autour de l'armure
    col_top = color_gradient(data["humidity_ext"], 0,100,(173,216,230),(0,0,139))
    col_bottom = color_gradient(data["temp_ext"], 0,100,(0,255,0),(0,0,255))
    cv2.ellipse(overlay, arm_center, (arm_width, arm_height), 0, 0, 180, col_top, 2)
    cv2.ellipse(overlay, arm_center, (arm_width, arm_height), 0, 180, 360, col_bottom, 2)

    # Tête
    head_top_left = (arm_center[0]-20, arm_center[1]-arm_height//2)
    head_bottom_right = (arm_center[0]+20, arm_center[1]-arm_height//2 + 40)
    head_edge_col = color_gradient(data["casque_temp"],0,100,(0,255,0),(0,0,255))
    head_fill_col = color_gradient(data["casque_humidity"],0,100,(173,216,230),(0,0,139))
    cv2.rectangle(overlay, head_top_left, head_bottom_right, head_edge_col, 3)
    cv2.rectangle(overlay, head_top_left, head_bottom_right, head_fill_col, -1)

    # Torse / Backpack
    torso_top_left = (arm_center[0]-20, arm_center[1]-30)
    torso_bottom_right = (arm_center[0]+20, arm_center[1]+60)
    torso_edge_col = color_gradient(data["backpack_temp"],0,100,(0,255,0),(0,0,255))
    torso_fill_col = color_gradient(data["humidity_ext"],0,100,(173,216,230),(0,0,139))
    cv2.rectangle(overlay, torso_top_left, torso_bottom_right, torso_edge_col,3)
    cv2.rectangle(overlay, torso_top_left, torso_bottom_right, torso_fill_col,-1)

    # Bras
    right_arm_top_left = (arm_center[0]+20, arm_center[1]-30)
    right_arm_bottom_right = (arm_center[0]+60, arm_center[1]+30)
    left_arm_top_left = (arm_center[0]-60, arm_center[1]-30)
    left_arm_bottom_right = (arm_center[0]-20, arm_center[1]+30)
    cv2.rectangle(overlay, right_arm_top_left, right_arm_bottom_right, (255,255,255),2)
    cv2.rectangle(overlay, left_arm_top_left, left_arm_bottom_right, (255,255,255),2)

    # Jambes
    right_leg_top_left = (arm_center[0], arm_center[1]+60)
    right_leg_bottom_right = (arm_center[0]+20, arm_center[1]+120)
    left_leg_top_left = (arm_center[0]-20, arm_center[1]+60)
    left_leg_bottom_right = (arm_center[0], arm_center[1]+120)
    cv2.rectangle(overlay, right_leg_top_left, right_leg_bottom_right, (255,255,255),2)
    cv2.rectangle(overlay, left_leg_top_left, left_leg_bottom_right, (255,255,255),2)

    # Symboles radioactifs
    col_ext = color_gradient(data["air_quality_ext"],0,2,(0,255,0),(0,0,255))
    col_int = color_gradient(data["air_quality_int"],0,2,(0,255,0),(0,0,255))
    cv2.circle(overlay, (arm_center[0]+arm_width+30, arm_center[1]-arm_height//2), 20, col_ext, -1)
    cv2.circle(overlay, (arm_center[0], arm_center[1]), 20, col_int, -1)

    # Fusion overlay
    cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)

    return frame
