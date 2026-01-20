"""
Sensor management for ESP32 Backpack
Handles all I2C sensors + MQ gas sensors
"""

from machine import I2C, Pin, PWM, ADC
import time
from config import *

class SensorManager:
    def __init__(self):
        # Initialize I2C
        self.i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=I2C_FREQ)
        
        # Fan control
        self.fan = PWM(Pin(FAN_PIN), freq=FAN_PWM_FREQ)
        self.fan.duty(0)
        
        # MQ sensors (analog)
        self.mq2_int = ADC(Pin(MQ2_INT_PIN))
        self.mq2_ext = ADC(Pin(MQ2_EXT_PIN))
        self.mq7_int = ADC(Pin(MQ7_INT_PIN))
        self.mq7_ext = ADC(Pin(MQ7_EXT_PIN))
        
        # Configure ADC
        self.mq2_int.atten(ADC.ATTN_11DB)  # 0-3.3V range
        self.mq2_ext.atten(ADC.ATTN_11DB)
        self.mq7_int.atten(ADC.ATTN_11DB)
        self.mq7_ext.atten(ADC.ATTN_11DB)
        
        # Detect sensors
        self.scan_sensors()
    
    def scan_sensors(self):
        \"\"\"Scan I2C bus\"\"\"
        devices = self.i2c.scan()
        print('I2C devices found:', [hex(d) for d in devices])
        
        self.has_bme280_int = BME280_INT_ADDR in devices
        self.has_ens160_int = ENS160_INT_ADDR in devices
        self.has_aht21_int = AHT21_INT_ADDR in devices
        self.has_ina219 = INA219_ADDR in devices
        self.has_pca9548a_int = PCA9548A_INT_ADDR in devices
    
    def read_bme280(self, interior=True):
        \"\"\"Read BME280 (interior or exterior)\"\"\"
        # TODO: Implement with proper library
        try:
            return {
                'temperature': 25.0,
                'humidity': 50.0,
                'pressure': 1013.25,
                'location': 'interior' if interior else 'exterior'
            }
        except Exception as e:
            print(f'Error reading BME280: {e}')
            return None
    
    def read_ens160(self, interior=True):
        \"\"\"Read ENS160 air quality\"\"\"
        # TODO: Implement
        try:
            return {
                'aqi': 1,
                'tvoc': 0,
                'eco2': 400,
                'location': 'interior' if interior else 'exterior'
            }
        except Exception as e:
            print(f'Error reading ENS160: {e}')
            return None
    
    def read_mq2(self, interior=True):
        \"\"\"Read MQ-2 smoke/gas sensor\"\"\"
        try:
            adc = self.mq2_int if interior else self.mq2_ext
            raw = adc.read()
            
            # Convert to approximate ppm (calibration needed)
            ppm = (raw / 4095) * 1000  # Placeholder formula
            
            return {
                'raw': raw,
                'ppm': ppm,
                'location': 'interior' if interior else 'exterior'
            }
        except Exception as e:
            print(f'Error reading MQ-2: {e}')
            return None
    
    def read_mq7(self, interior=True):
        \"\"\"Read MQ-7 CO sensor\"\"\"
        try:
            adc = self.mq7_int if interior else self.mq7_ext
            raw = adc.read()
            
            # Convert to CO ppm (calibration needed)
            co_ppm = (raw / 4095) * 200  # Placeholder formula
            
            return {
                'raw': raw,
                'co_ppm': co_ppm,
                'location': 'interior' if interior else 'exterior'
            }
        except Exception as e:
            print(f'Error reading MQ-7: {e}')
            return None
    
    def read_all(self):
        \"\"\"Read all sensors\"\"\"
        return {
            'bme280_int': self.read_bme280(interior=True),
            'bme280_ext': self.read_bme280(interior=False),
            'ens160_int': self.read_ens160(interior=True),
            'ens160_ext': self.read_ens160(interior=False),
            'mq2_int': self.read_mq2(interior=True),
            'mq2_ext': self.read_mq2(interior=False),
            'mq7_int': self.read_mq7(interior=True),
            'mq7_ext': self.read_mq7(interior=False)
        }
    
    def set_fan_speed(self, speed):
        \"\"\"Set fan speed (0-100%)\"\"\"
        duty = int((speed / 100) * 1023)
        self.fan.duty(duty)
        print(f'Fan speed set to {speed}%')
    
    def check_alerts(self, sensor_data):
        \"\"\"Check for dangerous gas levels\"\"\"
        alerts = []
        
        # Check CO levels (interior)
        mq7_int = sensor_data.get('mq7_int')
        if mq7_int and mq7_int['co_ppm'] > 50:
            alerts.append('⚠️  HIGH CO DETECTED INTERIOR!')
        
        # Check smoke (interior)
        mq2_int = sensor_data.get('mq2_int')
        if mq2_int and mq2_int['ppm'] > 300:
            alerts.append('⚠️  SMOKE DETECTED INTERIOR!')
        
        return alerts
