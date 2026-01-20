"""
ESP32 Backpack - Main Program
Environmental monitoring with multiple sensors
"""

import time
from sensors import SensorManager
from mqtt_client import MQTTHandler
from config import SENSOR_READ_INTERVAL

def main():
    print('=' * 40)
    print('ESP32 Backpack - Starting')
    print('=' * 40)
    
    # Initialize
    sensors = SensorManager()
    mqtt = MQTTHandler()
    
    # Connect MQTT
    if not mqtt.connect():
        print('MQTT connection failed. Retrying...')
        time.sleep(5)
        return
    
    print('System ready')
    
    loop_count = 0
    
    try:
        while True:
            loop_count += 1
            print(f'\n--- Loop {loop_count} ---')
            
            # Read all sensors
            sensor_data = sensors.read_all()
            
            # Check for alerts
            alerts = sensors.check_alerts(sensor_data)
            if alerts:
                for alert in alerts:
                    print(alert)
                    mqtt.publish('system/alerts', {'message': alert})
            
            # Publish data
            mqtt.publish_sensor_data(sensor_data)
            
            # Fan control based on interior temp
            bme_int = sensor_data.get('bme280_int')
            if bme_int and bme_int['temperature'] > 35:
                sensors.set_fan_speed(100)
            elif bme_int and bme_int['temperature'] > 30:
                sensors.set_fan_speed(70)
            elif bme_int and bme_int['temperature'] > 25:
                sensors.set_fan_speed(40)
            else:
                sensors.set_fan_speed(0)
            
            time.sleep(SENSOR_READ_INTERVAL)
    
    except KeyboardInterrupt:
        print('\nShutdown')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        sensors.set_fan_speed(0)
        mqtt.disconnect()

if __name__ == '__main__':
    main()
