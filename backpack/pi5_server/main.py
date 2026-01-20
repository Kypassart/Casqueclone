#!/usr/bin/env python3
"""
Backpack Pi 5 Server - Main entry point
Central server managing MQTT broker, YOLO detection, and WiFi AP
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))

import yaml
from logger import setup_logger

logger = setup_logger(__name__, 'logs/pi5_server.log')

def load_config():
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    logger.info("=" * 50)
    logger.info("Backpack Pi 5 Server - Starting")
    logger.info("=" * 50)
    
    config = load_config()
    logger.info(f"Configuration loaded")
    
    # TODO: Initialize
    # - MQTT broker (Mosquitto via subprocess or paho)
    # - YOLO model
    # - WiFi AP (via hostapd/dnsmasq scripts)
    
    logger.info("Server ready - Press Ctrl+C to stop")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        logger.info("Server stopped")

if __name__ == '__main__':
    main()
