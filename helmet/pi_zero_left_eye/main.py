#!/usr/bin/env python3
"""
Helmet Left Eye - Main entry point
Manages HUD display, camera streaming, and MQTT communication
"""

import sys
import time
from pathlib import Path

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))

import yaml
from logger import setup_logger
from mqtt_topics import *

logger = setup_logger(__name__, 'logs/left_eye.log')

def load_config():
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info("Helmet Left Eye HUD System - Starting")
    logger.info("=" * 50)
    
    config = load_config()
    logger.info(f"Configuration loaded: {config}")
    
    # TODO: Initialize components
    # - MQTT client
    # - Camera handler
    # - HUD display
    
    try:
        logger.info("Entering main loop...")
        while True:
            # TODO: Main loop logic
            # - Capture frame
            # - Send to MQTT
            # - Update HUD
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up...")
        # TODO: Cleanup resources

if __name__ == '__main__':
    main()
