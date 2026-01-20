"""
Boot script - Executed on power-up
Connects to WiFi
"""

import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

def connect_wifi():
    \"\"\"Connect to WiFi network\"\"\"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to WiFi:', WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print('.', end='')
        
        print()
    
    if wlan.isconnected():
        print('WiFi connected!')
        print('IP:', wlan.ifconfig()[0])
        return True
    else:
        print('WiFi connection failed')
        return False

# Auto-connect on boot
connect_wifi()
