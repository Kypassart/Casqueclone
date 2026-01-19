#!/usr/bin/env python3
"""
OLED Identifier - Clone Trooper AR Project
Identifie votre écran OLED 2.42" IIC Ver:1.1

Usage: python3 oled_identifier.py
"""

import board
import busio
import sys
from time import sleep

# Couleurs terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Affiche bannière"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("    CLONE TROOPER AR - OLED IDENTIFIER")
    print("=" * 60)
    print(f"{Colors.END}")

def scan_i2c():
    """
    Scanne le bus I2C pour trouver devices
    Returns: Liste adresses trouvées
    """
    print(f"\n{Colors.BLUE} Scan du bus I2C...{Colors.END}")
    
    try:
        # Créer bus I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Verrouiller bus
        while not i2c.try_lock():
            pass
        
        # Scanner
        devices = i2c.scan()
        
        # Déverrouiller
        i2c.unlock()
        
        if devices:
            print(f"{Colors.GREEN}v {len(devices)} device(s) trouvé(s){Colors.END}")
            for addr in devices:
                hex_addr = hex(addr)
                print(f"   Adresse: {hex_addr} (décimal: {addr})")
            return devices
        else:
            print(f"{Colors.RED}X Aucun device I2C trouvé{Colors.END}")
            print(f"\n{Colors.YELLOW}Vérifiez:{Colors.END}")
            print("  1. I2C activé : sudo raspi-config > Interface Options > I2C")
            print("  2. Câblage correct")
            print("  3. Alimentation OLED (VCC sur 3.3V)")
            return []
            
    except Exception as e:
        print(f"{Colors.RED}X Erreur scan I2C: {e}{Colors.END}")
        return []

def identify_controller(addr):
    """
    Identifie le contrôleur OLED selon adresse
    """
    controllers = {
        0x3C: "SSD1306 ou SSD1309 (très probable)",
        0x3D: "SSD1306 ou SSD1309 (adresse modifiée)",
        0x78: "SH1106 (mode adressage différent)",
        0x7A: "SH1106 (adresse modifiée)"
    }
    
    return controllers.get(addr, "Contrôleur inconnu")

def test_display_ssd1306(addr=0x3C):
    """
    Teste affichage avec driver SSD1306
    Compatible SSD1309 aussi (protocole identique)
    """
    print(f"\n{Colors.BLUE} Test avec driver SSD1306/1309...{Colors.END}")
    
    try:
        import adafruit_ssd1306
        from PIL import Image, ImageDraw, ImageFont
        
        # Créer bus I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Créer objet OLED
        # Résolution standard : 128x64
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=addr)
        
        print(f"{Colors.GREEN}v Driver SSD1306/1309 chargé{Colors.END}")
        print(f"  Résolution: 128x64 pixels")
        
        # Test 1 : Écran blanc
        print(f"\n{Colors.YELLOW}Test 1: Écran blanc (2s)...{Colors.END}")
        oled.fill(1)  # Blanc
        oled.show()
        sleep(2)
        
        # Test 2 : Écran noir
        print(f"{Colors.YELLOW}Test 2: Écran noir (2s)...{Colors.END}")
        oled.fill(0)  # Noir
        oled.show()
        sleep(2)
        
        # Test 3 : Texte
        print(f"{Colors.YELLOW}Test 3: Affichage texte (3s)...{Colors.END}")
        image = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "CLONE", font=font, fill=1)
        draw.text((10, 30), "TROOPER", font=font, fill=1)
        
        oled.image(image)
        oled.show()
        sleep(3)
        
        # Test 4 : Formes
        print(f"{Colors.YELLOW}Test 4: Formes géométriques (3s)...{Colors.END}")
        image = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(image)
        
        # Rectangle
        draw.rectangle([10, 10, 50, 30], outline=1, fill=0)
        # Cercle
        draw.ellipse([60, 10, 90, 40], outline=1, fill=0)
        # Ligne
        draw.line([10, 45, 118, 45], fill=1, width=2)
        
        oled.image(image)
        oled.show()
        sleep(3)
        
        # Nettoyer
        oled.fill(0)
        oled.show()
        
        print(f"{Colors.GREEN}v Tous les tests réussis !{Colors.END}")
        return True
        
    except ImportError:
        print(f"{Colors.RED}X Bibliothèque manquante{Colors.END}")
        print(f"\nInstaller avec:")
        print(f"  pip3 install adafruit-circuitpython-ssd1306 pillow")
        return False
        
    except Exception as e:
        print(f"{Colors.RED}X Erreur test: {e}{Colors.END}")
        return False

def test_display_sh1106(addr=0x3C):
    """
    Teste affichage avec driver SH1106
    (Si SSD1306 ne fonctionne pas)
    """
    print(f"\n{Colors.BLUE} Test avec driver SH1106...{Colors.END}")
    
    try:
        import adafruit_ssd1306  # SH1106 utilise même lib
        from PIL import Image, ImageDraw, ImageFont
        
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # SH1106 a une résolution 132x64 mais on utilise 128x64
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=addr)
        
        print(f"{Colors.GREEN}v Driver SH1106 chargé{Colors.END}")
        
        # Test simple
        oled.fill(1)
        oled.show()
        sleep(1)
        oled.fill(0)
        oled.show()
        
        print(f"{Colors.GREEN}v Test SH1106 réussi{Colors.END}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}X Erreur test SH1106: {e}{Colors.END}")
        return False

def generate_report(devices, test_results):
    """
    Génère rapport identification
    """
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("    RAPPORT D'IDENTIFICATION")
    print("=" * 60)
    print(f"{Colors.END}")
    
    if not devices:
        print(f"{Colors.RED}  Aucun OLED détecté{Colors.END}")
        print(f"\n{Colors.YELLOW}Actions recommandées:{Colors.END}")
        print("  1. Vérifier câblage (VCC, GND, SCL, SDA)")
        print("  2. Activer I2C : sudo raspi-config")
        print("  3. Redémarrer Pi")
        return
    
    print(f"\n{Colors.GREEN}v OLED détecté et fonctionnel{Colors.END}\n")
    
    addr = devices[0]
    print(f" Adresse I2C     : {hex(addr)}")
    print(f" Contrôleur      : {identify_controller(addr)}")
    print(f" Résolution      : 128x64 pixels")
    print(f" Taille          : 2.42 pouces (estimé)")
    print(f" Type            : Monochrome (Blanc ou Bleu)")
    print(f" Interface       : I2C (IIC)")
    
    if test_results.get('ssd1306'):
        print(f"\n{Colors.GREEN} Compatible SSD1306/SSD1309{Colors.END}")
        print(f"\n{Colors.YELLOW}Code à utiliser:{Colors.END}")
        print(f"""
import board
import busio
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr={hex(addr)})
        """)
    
    print(f"\n{Colors.BLUE} Fichier config généré: oled_config.py{Colors.END}")
    
    # Générer fichier config
    with open("oled_config.py", "w") as f:
        f.write(f"""# Configuration OLED 2.42" - Clone Trooper AR
# Généré automatiquement

OLED_I2C_ADDRESS = {hex(addr)}
OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_CONTROLLER = "SSD1309"  # ou SSD1306 (compatible)
""")
    
    print(f"{Colors.GREEN}v Configuration sauvegardée{Colors.END}")

def main():
    """
    Fonction principale
    """
    print_header()
    
    # Vérifier bibliothèques
    try:
        import adafruit_ssd1306
        from PIL import Image
    except ImportError:
        print(f"{Colors.RED}X Bibliothèques manquantes{Colors.END}\n")
        print("Installer avec:")
        print("  sudo apt-get install -y python3-pip i2c-tools")
        print("  pip3 install adafruit-circuitpython-ssd1306 pillow")
        sys.exit(1)
    
    # Scanner I2C
    devices = scan_i2c()
    
    if not devices:
        print(f"\n{Colors.YELLOW} Astuce: Tester manuellement I2C{Colors.END}")
        print("  sudo i2cdetect -y 1")
        sys.exit(1)
    
    # Identifier contrôleur
    print(f"\n{Colors.BLUE} Identification contrôleur...{Colors.END}")
    for addr in devices:
        controller = identify_controller(addr)
        print(f"  {hex(addr)}: {controller}")
    
    # Tester affichage
    test_results = {}
    
    primary_addr = devices[0]
    
    # Tester SSD1306/1309 (le plus courant)
    if test_display_ssd1306(primary_addr):
        test_results['ssd1306'] = True
    else:
        # Essayer SH1106
        test_results['sh1106'] = test_display_sh1106(primary_addr)
    
    # Générer rapport
    generate_report(devices, test_results)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD} Identification terminée !{Colors.END}\n")
    print(f"{Colors.BLUE}Prochaines étapes:{Colors.END}")
    print("  1. Utiliser oled_config.py dans vos scripts")
    print("  2. Tester HUD demo : python3 basic_hud_demo.py")
    print("  3. Développer modes HUD personnalisés")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW} Arrêt utilisateur{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}X Erreur critique: {e}{Colors.END}")
        sys.exit(1)