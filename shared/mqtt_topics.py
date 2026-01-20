"""
MQTT Topics definition for Casqueclone armor system
Centralized topic naming convention
"""

# Helmet topics
HELMET_RIGHT_FRAME = "helmet/right/frame"
HELMET_RIGHT_TEMP = "helmet/right/temp"
HELMET_RIGHT_HUMIDITY = "helmet/right/humidity"
HELMET_LEFT_FRAME = "helmet/left/frame"
HELMET_LEFT_TEMP = "helmet/left/temp"
HELMET_ORIENTATION = "helmet/orientation"
HELMET_AIR_QUALITY = "helmet/air_quality"

# Backpack topics  
BACKPACK_YOLO_RESULTS = "backpack/yolo/results"
BACKPACK_TEMP_INT = "backpack/temp/interior"
BACKPACK_TEMP_EXT = "backpack/temp/exterior"
BACKPACK_GAS_CO_INT = "backpack/gas/co/interior"
BACKPACK_GAS_CO_EXT = "backpack/gas/co/exterior"
BACKPACK_GAS_SMOKE_INT = "backpack/gas/smoke/interior"
BACKPACK_GAS_SMOKE_EXT = "backpack/gas/smoke/exterior"

# Arm display topics
ARM_COMMAND = "arm/command"
ARM_STATUS = "arm/status"

# Energy topics
ENERGY_BATTERY_LEVEL = "energy/battery/level"
ENERGY_BATTERY_VOLTAGE = "energy/battery/voltage"
ENERGY_BATTERY_CURRENT = "energy/battery/current"
ENERGY_POWER_CONSUMPTION = "energy/power/consumption"

# System topics
SYSTEM_STATUS = "system/status"
SYSTEM_COMMAND = "system/command"
