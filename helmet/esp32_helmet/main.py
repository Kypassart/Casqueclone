"""
ESP32 Helmet - Main Program
Reads sensors and publishes to MQTT
"""

import time
from sensors import SensorManager
from mqtt_client import MQTTHandler
from config import SENSOR_READ_INTERVAL

def main():
    print('=' * 40)
    print('ESP32 Helmet - Starting')
    print('=' * 40)
    
    # Initialize components
    sensors = SensorManager()
    mqtt = MQTTHandler()
    
    # Connect to MQTT
    if not mqtt.connect():
        print('Failed to connect to MQTT. Retrying in 5s...')
        time.sleep(5)
        return
    
    print('System ready. Entering main loop...')
    
    loop_count = 0
    
    try:
        while True:
            loop_count += 1
            print(f'\n--- Loop {loop_count} ---')
            
            # Read all sensors
            sensor_data = sensors.read_all()
            
            # Publish to MQTT
            mqtt.publish_sensor_data(sensor_data)
            
            # Fan control based on temperature
            env = sensor_data.get('environment')
            if env and env['temperature'] > 30:
                sensors.set_fan_speed(100)  # Full speed
            elif env and env['temperature'] > 25:
                sensors.set_fan_speed(50)   # Half speed
            else:
                sensors.set_fan_speed(0)    # Off
            
            # Wait
            time.sleep(SENSOR_READ_INTERVAL)
    
    except KeyboardInterrupt:
        print('\nShutdown requested')
    except Exception as e:
        print(f'Error in main loop: {e}')
    finally:
        sensors.set_fan_speed(0)
        mqtt.disconnect()
        print('ESP32 stopped')

# Run main program
if __name__ == '__main__':
    main()
