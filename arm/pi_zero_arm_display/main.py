#!/usr/bin/env python3
"""
Arm Display - Touchscreen control interface
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))

import yaml
from logger import setup_logger

logger = setup_logger(__name__, 'logs/arm_display.log')

def load_config():
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    logger.info("Arm Display Interface - Starting")
    
    config = load_config()
    
    # TODO: Initialize
    # - Pygame display
    # - MQTT client
    # - Touch handlers
    
    logger.info("Interface ready")
    
    try:
        import time
        while True:
            # TODO: Main GUI loop
            time.sleep(0.033)  # ~30 FPS
    except KeyboardInterrupt:
        logger.info("Shutdown")

if __name__ == '__main__':
    main()
