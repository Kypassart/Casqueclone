#!/usr/bin/env python3
"""
Basic HUD Demo - Clone Trooper AR Project
Démonstration des 4 modes HUD sur OLED 2.42"

Modes:
  0 - Minimal (Patrouille)
  1 - Combat (Menace détectée)
  2 - Navigation (Déplacement)
  3 - Détection IA (Analyse)

Contrôles:
  - Mode change automatique toutes les 10s
  - Ctrl+C pour quitter

Usage: python3 basic_hud_demo.py
"""

import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time
import math
import random
from datetime import datetime

# Couleurs terminal pour debug
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class HUDSimulator:
    """
    Simulateur HUD Clone Trooper
    Génère données factices et affiche 4 modes
    """
    
    def __init__(self):
        """Initialisation"""
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("=" * 60)
        print("    CLONE TROOPER AR - HUD DEMO")
        print("=" * 60)
        print(f"{Colors.END}")
        
        # Charger config OLED
        try:
            from oled_config import OLED_I2C_ADDRESS, OLED_WIDTH, OLED_HEIGHT
            self.WIDTH = OLED_WIDTH
            self.HEIGHT = OLED_HEIGHT
            self.ADDR = OLED_I2C_ADDRESS
            print(f"{Colors.GREEN}v Config chargée: {OLED_WIDTH}x{OLED_HEIGHT} @ {hex(OLED_I2C_ADDRESS)}{Colors.END}")
        except ImportError:
            # Valeurs par défaut
            self.WIDTH = 128
            self.HEIGHT = 64
            self.ADDR = 0x3C
            print(f"{Colors.YELLOW} Config par défaut: 128x64 @ 0x3C{Colors.END}")
        
        # Initialiser OLED
        print(f"{Colors.BLUE} Connexion OLED...{Colors.END}")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            self.WIDTH, self.HEIGHT, i2c, addr=self.ADDR
        )
        print(f"{Colors.GREEN}v OLED connecté{Colors.END}")
        
        # Charger polices
        try:
            self.font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8
            )
            self.font_medium = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10
            )
            self.font_large = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14
            )
            print(f"{Colors.GREEN}v Polices TrueType chargées{Colors.END}")
        except:
            # Police par défaut si échec
            self.font_small = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            print(f"{Colors.YELLOW} Polices par défaut{Colors.END}")
        
        # État simulation
        self.mode = 0  # Mode HUD actuel
        self.blink_state = False  # Pour clignotement
        
        # Données simulées
        self.data = {
            'persons': 0,
            'temp': 22.0,
            'humidity': 45,
            'battery': 68,
            'heading': 45,  # Boussole 0-359°
            'armor': 80,
            'weapon': False,
            'weapon_type': '',
            'fps': 0
        }
        
        # Stats
        self.frame_count = 0
        self.start_time = time.time()
        
        print(f"{Colors.GREEN}v Initialisation terminée{Colors.END}\n")
    
    def simulate_data(self):
        """
        Génère données factices réalistes
        Simule changements progressifs
        """
        # Température varie lentement
        self.data['temp'] += random.uniform(-0.1, 0.1)
        self.data['temp'] = max(15, min(35, self.data['temp']))
        
        # Humidité varie
        self.data['humidity'] += random.randint(-1, 1)
        self.data['humidity'] = max(20, min(80, self.data['humidity']))
        
        # Batterie décroît lentement
        if random.random() < 0.01:  # 1% chance par frame
            self.data['battery'] = max(0, self.data['battery'] - 1)
        
        # Boussole tourne
        self.data['heading'] = (self.data['heading'] + 1) % 360
        
        # Personnes détectées (change parfois)
        if random.random() < 0.05:  # 5% chance
            self.data['persons'] = random.randint(0, 3)
        
        # Arme détectée (rare)
        if random.random() < 0.02:  # 2% chance
            self.data['weapon'] = not self.data['weapon']
            if self.data['weapon']:
                self.data['weapon_type'] = random.choice(['RIFLE', 'PISTOL'])
        
        # FPS
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            elapsed = time.time() - self.start_time
            self.data['fps'] = 30 / elapsed
            self.start_time = time.time()
    
    def draw_compass(self, draw, x, y, radius, heading):
        """Dessine boussole circulaire"""
        # Cercle
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            outline=1, width=1
        )
        
        # Marqueurs N, E, S, W
        directions = ['N', 'E', 'S', 'W']
        angles = [0, 90, 180, 270]
        
        for direction, angle in zip(directions, angles):
            rad = math.radians(angle - heading)
            dx = int(x + (radius - 5) * math.sin(rad))
            dy = int(y - (radius - 5) * math.cos(rad))
            draw.text((dx - 2, dy - 3), direction, font=self.font_small, fill=1)
        
        # Flèche Nord
        north_rad = math.radians(-heading)
        arrow_x = int(x + (radius - 2) * math.sin(north_rad))
        arrow_y = int(y - (radius - 2) * math.cos(north_rad))
        draw.line([x, y, arrow_x, arrow_y], fill=1, width=2)
    
    def draw_battery(self, draw, x, y, level):
        """Dessine indicateur batterie"""
        # Contour
        draw.rectangle([x, y, x + 20, y + 8], outline=1)
        # Borne
        draw.rectangle([x + 20, y + 2, x + 22, y + 6], fill=1)
        # Remplissage
        fill_w = int((level / 100) * 16)
        if fill_w > 0:
            draw.rectangle([x + 2, y + 2, x + 2 + fill_w, y + 6], fill=1)
    
    def draw_person_icon(self, draw, x, y):
        """Dessine icône personne"""
        # Tête
        draw.ellipse([x - 2, y - 4, x + 2, y], outline=1)
        # Corps
        draw.line([x, y, x, y + 8], fill=1)
        # Bras
        draw.line([x - 4, y + 3, x + 4, y + 3], fill=1)
        # Jambes
        draw.line([x, y + 8, x - 3, y + 12], fill=1)
        draw.line([x, y + 8, x + 3, y + 12], fill=1)
    
    def draw_mode_0_minimal(self, draw):
        """Mode 0 : Minimal (Patrouille)"""
        # HAUT : Info essentielles
        draw.text((2, 2), f"P:{self.data['persons']}", 
                 font=self.font_medium, fill=1)
        
        if self.data['persons'] > 0:
            self.draw_person_icon(draw, 18, 8)
        
        draw.text((30, 2), f"{self.data['temp']:.0f}C", 
                 font=self.font_small, fill=1)
        
        # Boussole
        self.draw_compass(draw, 70, 8, 5, self.data['heading'])
        draw.text((78, 2), f"{self.data['heading']:03d}", 
                 font=self.font_small, fill=1)
        
        # Batterie
        self.draw_battery(draw, 102, 3, self.data['battery'])
        
        # CENTRE : Crosshair
        cx, cy = 64, 32
        draw.line([cx - 6, cy, cx + 6, cy], fill=1)
        draw.line([cx, cy - 6, cx, cy + 6], fill=1)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], outline=1)
        
        # BAS : Armure + FPS
        draw.text((2, 54), "ARM:", font=self.font_small, fill=1)
        draw.rectangle([22, 54, 60, 60], outline=1)
        fill_w = int((self.data['armor'] / 100) * 36)
        if fill_w > 0:
            draw.rectangle([23, 55, 23 + fill_w, 59], fill=1)
        
        draw.text((85, 54), f"{self.data['fps']:.0f}F", 
                 font=self.font_small, fill=1)
    
    def draw_mode_1_combat(self, draw):
        """Mode 1 : Combat (Menace)"""
        # Détections
        draw.text((2, 2), f"HOSTIL:{self.data['persons']}", 
                 font=self.font_medium, fill=1)
        
        # Alerte arme (clignotant)
        if self.data['weapon'] and self.blink_state:
            # Triangle
            draw.polygon([(6, 14), (2, 20), (10, 20)], outline=1)
            draw.text((14, 16), "ARMED", font=self.font_small, fill=1)
        
        # Crosshair renforcé
        cx, cy = 64, 32
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=1)
        draw.line([cx, cy - 14, cx, cy - 10], fill=1, width=2)
        draw.line([cx, cy + 10, cx, cy + 14], fill=1, width=2)
        draw.line([cx - 14, cy, cx - 10, cy], fill=1, width=2)
        draw.line([cx + 10, cy, cx + 14, cy], fill=1, width=2)
        draw.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=1)
        
        # Barres de vie segmentées
        for i in range(10):
            filled = i < (self.data['armor'] // 10)
            if filled:
                draw.rectangle([6 + i * 5, 52, 9 + i * 5, 60], fill=1)
            else:
                draw.rectangle([6 + i * 5, 52, 9 + i * 5, 60], outline=1)
        
        # Radar mini
        rx, ry = 105, 52
        draw.ellipse([rx - 8, ry - 8, rx + 8, ry + 8], outline=1)
        draw.line([rx - 8, ry, rx + 8, ry], fill=1)
        draw.line([rx, ry - 8, rx, ry + 8], fill=1)
        
        # Blips
        if self.data['persons'] > 0:
            draw.ellipse([rx + 3, ry - 3, rx + 5, ry - 1], fill=1)
    
    def draw_mode_2_navigation(self, draw):
        """Mode 2 : Navigation"""
        # Boussole grande
        self.draw_compass(draw, 64, 16, 12, self.data['heading'])
        draw.text((52, 32), f"{self.data['heading']:03d}°", 
                 font=self.font_medium, fill=1)
        
        # Info nav
        draw.text((5, 48), "WPT:2.5km", font=self.font_small, fill=1)
        draw.text((5, 56), "SPD:4", font=self.font_small, fill=1)
        draw.text((80, 56), "ALT:8m", font=self.font_small, fill=1)
        
        # Ligne horizon
        draw.line([20, 32, 108, 32], fill=1)
        draw.rectangle([62, 30, 66, 34], fill=1)
    
    def draw_mode_3_detection(self, draw):
        """Mode 3 : Détection IA"""
        # Info détections
        draw.text((2, 2), f"DET:{self.data['persons']}", 
                 font=self.font_medium, fill=1)
        draw.text((35, 2), "IA:ON", font=self.font_small, fill=1)
        draw.text((65, 2), f"{self.data['fps']:.0f}FPS", 
                 font=self.font_small, fill=1)
        
        # Bounding boxes simulées
        if self.data['persons'] > 0:
            draw.rectangle([20, 16, 45, 42], outline=1)
            draw.text((22, 14), "92%", font=self.font_small, fill=1)
        
        if self.data['persons'] > 1:
            draw.rectangle([70, 18, 90, 40], outline=1)
            draw.text((72, 16), "78%", font=self.font_small, fill=1)
        
        # Type arme
        if self.data['weapon']:
            draw.text((2, 54), f"WEAP:{self.data['weapon_type']}", 
                     font=self.font_small, fill=1)
        
        # Confiance
        draw.text((70, 54), "CONF:", font=self.font_small, fill=1)
        draw.rectangle([100, 54, 122, 60], outline=1)
        draw.rectangle([101, 55, 118, 59], fill=1)
    
    def render_frame(self):
        """Génère et affiche une frame"""
        # Créer image
        image = Image.new("1", (self.WIDTH, self.HEIGHT))
        draw = ImageDraw.Draw(image)
        
        # Dessiner selon mode
        if self.mode == 0:
            self.draw_mode_0_minimal(draw)
        elif self.mode == 1:
            self.draw_mode_1_combat(draw)
        elif self.mode == 2:
            self.draw_mode_2_navigation(draw)
        elif self.mode == 3:
            self.draw_mode_3_detection(draw)
        
        # Indicateur mode (coin bas droit)
        mode_names = ['MIN', 'CMB', 'NAV', 'DET']
        draw.text((110, 2), mode_names[self.mode], 
                 font=self.font_small, fill=1)
        
        # Envoyer à OLED
        self.oled.image(image)
        self.oled.show()
    
    def run(self):
        """Boucle principale"""
        print(f"{Colors.GREEN} Démarrage démo HUD...{Colors.END}\n")
        print("Modes:")
        print("  0 - Minimal (Patrouille)")
        print("  1 - Combat (Menace)")
        print("  2 - Navigation")
        print("  3 - Détection IA")
        print("\nChangement automatique toutes les 10s")
        print("Appuyez Ctrl+C pour quitter\n")
        
        mode_start = time.time()
        blink_timer = time.time()
        
        try:
            while True:
                # Simuler données
                self.simulate_data()
                
                # Render frame
                self.render_frame()
                
                # Blink animation (500ms)
                if time.time() - blink_timer > 0.5:
                    self.blink_state = not self.blink_state
                    blink_timer = time.time()
                
                # Changer mode toutes les 10s
                if time.time() - mode_start > 10:
                    self.mode = (self.mode + 1) % 4
                    mode_names = ['Minimal', 'Combat', 'Navigation', 'Détection']
                    print(f"{Colors.BLUE}-> Mode {self.mode}: {mode_names[self.mode]}{Colors.END}")
                    mode_start = time.time()
                
                # Limiter FPS (~30)
                time.sleep(0.033)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW} Arrêt demandé{Colors.END}")
            self.cleanup()
    
    def cleanup(self):
        """Nettoyage avant arrêt"""
        print(f"{Colors.BLUE} Nettoyage...{Colors.END}")
        self.oled.fill(0)
        self.oled.show()
        print(f"{Colors.GREEN}v Démo terminée{Colors.END}")

def main():
    """Point d'entrée"""
    try:
        demo = HUDSimulator()
        demo.run()
    except Exception as e:
        print(f"{Colors.RED}X Erreur: {e}{Colors.END}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()