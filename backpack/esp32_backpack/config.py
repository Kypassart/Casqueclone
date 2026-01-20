"""
Configuration for ESP32 Backpack
"""

# WiFi
WIFI_SSID = 'CloneTrooper-HUD'
WIFI_PASSWORD = 'Order66Execute'

# MQTT
MQTT_BROKER = '192.168.4.1'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp32_backpack'

# I2C
I2C_SDA = 21
I2C_SCL = 22
I2C_FREQ = 100000

# Sensors I2C addresses
BME280_INT_ADDR = 0x76  # Intérieur
BME280_EXT_ADDR = 0x77  # Extérieur (via multiplexeur)
ENS160_INT_ADDR = 0x53  # Intérieur
ENS160_EXT_ADDR = 0x52  # Extérieur (via multiplexeur)
AHT21_INT_ADDR = 0x38   # Intérieur
AHT21_EXT_ADDR = 0x39   # Extérieur (via multiplexeur)
INA219_ADDR = 0x40
PCA9548A_INT_ADDR = 0x70  # Multiplexeur intérieur
PCA9548A_EXT_ADDR = 0x71  # Multiplexeur extérieur

# MQ Sensors (Analog)
MQ2_INT_PIN = 34  # ADC1_CH6
MQ2_EXT_PIN = 35  # ADC1_CH7
MQ7_INT_PIN = 32  # ADC1_CH4
MQ7_EXT_PIN = 33  # ADC1_CH5

# Ventilateur
FAN_PIN = 25
FAN_PWM_FREQ = 25000

# Timing
SENSOR_READ_INTERVAL = 2  # secondes (plus de capteurs = plus lent)
