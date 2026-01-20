"""
MQTT Client for ESP32 Backpack
"""

from umqtt.simple import MQTTClient
import json
from config import MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID

class MQTTHandler:
    def __init__(self):
        self.client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
        self.connected = False
    
    def connect(self):
        \"\"\"Connect to MQTT broker\"\"\"
        try:
            self.client.connect()
            self.connected = True
            print('MQTT connected')
            return True
        except Exception as e:
            print(f'MQTT failed: {e}')
            return False
    
    def disconnect(self):
        \"\"\"Disconnect\"\"\"
        try:
            self.client.disconnect()
            self.connected = False
        except:
            pass
    
    def publish(self, topic, data):
        \"\"\"Publish to topic\"\"\"
        if not self.connected:
            return False
        
        try:
            payload = json.dumps(data)
            self.client.publish(topic, payload)
            return True
        except Exception as e:
            print(f'Publish error: {e}')
            return False
    
    def publish_sensor_data(self, sensor_data):
        \"\"\"Publish all backpack sensor data\"\"\"
        
        # BME280 interior
        if sensor_data.get('bme280_int'):
            self.publish('backpack/temp/interior', sensor_data['bme280_int'])
        
        # BME280 exterior
        if sensor_data.get('bme280_ext'):
            self.publish('backpack/temp/exterior', sensor_data['bme280_ext'])
        
        # Air quality interior
        if sensor_data.get('ens160_int'):
            self.publish('backpack/air_quality/interior', sensor_data['ens160_int'])
        
        # Air quality exterior
        if sensor_data.get('ens160_ext'):
            self.publish('backpack/air_quality/exterior', sensor_data['ens160_ext'])
        
        # Gas sensors
        if sensor_data.get('mq2_int'):
            self.publish('backpack/gas/smoke/interior', sensor_data['mq2_int'])
        
        if sensor_data.get('mq2_ext'):
            self.publish('backpack/gas/smoke/exterior', sensor_data['mq2_ext'])
        
        if sensor_data.get('mq7_int'):
            self.publish('backpack/gas/co/interior', sensor_data['mq7_int'])
        
        if sensor_data.get('mq7_ext'):
            self.publish('backpack/gas/co/exterior', sensor_data['mq7_ext'])
