"""
MQTT Client for ESP32
Handles connection and publishing sensor data
"""

from umqtt.simple import MQTTClient
import json
import time
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
            print('MQTT connected to', MQTT_BROKER)
            return True
        except Exception as e:
            print(f'MQTT connection failed: {e}')
            self.connected = False
            return False
    
    def disconnect(self):
        \"\"\"Disconnect from broker\"\"\"
        try:
            self.client.disconnect()
            self.connected = False
            print('MQTT disconnected')
        except:
            pass
    
    def publish(self, topic, data):
        \"\"\"
        Publish data to MQTT topic
        
        Args:
            topic: MQTT topic string
            data: Dictionary to publish (will be JSON encoded)
        \"\"\"
        if not self.connected:
            print('Not connected to MQTT')
            return False
        
        try:
            payload = json.dumps(data)
            self.client.publish(topic, payload)
            print(f'Published to {topic}: {payload[:50]}...')
            return True
        except Exception as e:
            print(f'Publish error: {e}')
            return False
    
    def publish_sensor_data(self, sensor_data):
        \"\"\"Publish all sensor data to appropriate topics\"\"\"
        
        # Orientation
        if sensor_data.get('orientation'):
            self.publish('helmet/orientation', sensor_data['orientation'])
        
        # Environment (BME280)
        if sensor_data.get('environment'):
            env = sensor_data['environment']
            self.publish('helmet/temp', {'value': env['temperature']})
            self.publish('helmet/humidity', {'value': env['humidity']})
            self.publish('helmet/pressure', {'value': env['pressure']})
        
        # Air quality
        if sensor_data.get('air_quality'):
            self.publish('helmet/air_quality', sensor_data['air_quality'])
        
        # Power
        if sensor_data.get('power'):
            self.publish('helmet/power', sensor_data['power'])
