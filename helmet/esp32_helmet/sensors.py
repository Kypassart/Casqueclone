"""
Sensor management for ESP32 Helmet
Handles all I2C sensors
"""

from machine import I2C, Pin, PWM
import time
from config import *

class SensorManager:
    def __init__(self):
        # Initialize I2C
        self.i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=I2C_FREQ)
        
        # Fan control
        self.fan = PWM(Pin(FAN_PIN), freq=FAN_PWM_FREQ)
        self.fan.duty(0)  # Start off
        
        # Detect sensors
        self.scan_sensors()
    
    def scan_sensors(self):
        \"\"\"Scan I2C bus for connected devices\"\"\"
        devices = self.i2c.scan()
        print('I2C devices found:', [hex(d) for d in devices])
        
        self.has_bno055 = BNO055_ADDR in devices
        self.has_bme280 = BME280_ADDR in devices
        self.has_ens160 = ENS160_ADDR in devices
        self.has_aht21 = AHT21_ADDR in devices
        self.has_ina219 = INA219_ADDR in devices
        self.has_pca9548a = PCA9548A_ADDR in devices
    
    def read_bno055(self):
        \"\"\"Read orientation from BNO055\"\"\"
        if not self.has_bno055:
            return None
        
        # TODO: Implement BNO055 reading
        # Simple example (you'll need proper BNO055 library)
        try:
            # Placeholder
            return {
                'heading': 0.0,
                'roll': 0.0,
                'pitch': 0.0
            }
        except Exception as e:
            print(f'Error reading BNO055: {e}')
            return None
    
    def read_bme280(self):
        \"\"\"Read temp/humidity/pressure from BME280\"\"\"
        if not self.has_bme280:
            return None
        
        # TODO: Implement BME280 reading
        try:
            return {
                'temperature': 25.0,
                'humidity': 50.0,
                'pressure': 1013.25
            }
        except Exception as e:
            print(f'Error reading BME280: {e}')
            return None
    
    def read_ens160(self):
        \"\"\"Read air quality from ENS160\"\"\"
        if not self.has_ens160:
            return None
        
        # TODO: Implement ENS160 reading
        try:
            return {
                'aqi': 1,  # Air Quality Index
                'tvoc': 0,  # Total VOC
                'eco2': 400  # eCO2
            }
        except Exception as e:
            print(f'Error reading ENS160: {e}')
            return None
    
    def read_aht21(self):
        \"\"\"Read temp/humidity from AHT21\"\"\"
        if not self.has_aht21:
            return None
        
        # TODO: Implement AHT21 reading
        try:
            return {
                'temperature': 25.0,
                'humidity': 50.0
            }
        except Exception as e:
            print(f'Error reading AHT21: {e}')
            return None
    
    def read_ina219(self):
        \"\"\"Read power metrics from INA219\"\"\"
        if not self.has_ina219:
            return None
        
        # TODO: Implement INA219 reading
        try:
            return {
                'voltage': 3.7,
                'current': 0.5,
                'power': 1.85
            }
        except Exception as e:
            print(f'Error reading INA219: {e}')
            return None
    
    def read_all(self):
        \"\"\"Read all sensors\"\"\"
        return {
            'orientation': self.read_bno055(),
            'environment': self.read_bme280(),
            'air_quality': self.read_ens160(),
            'aht21': self.read_aht21(),
            'power': self.read_ina219()
        }
    
    def set_fan_speed(self, speed):
        \"\"\"
        Set fan speed (0-100%)
        
        Args:
            speed: Integer 0-100
        \"\"\"
        duty = int((speed / 100) * 1023)
        self.fan.duty(duty)
        print(f'Fan speed set to {speed}%')
