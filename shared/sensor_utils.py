"""
Common sensor utilities and helper functions
"""

import time
from typing import Dict, Any

def safe_read_sensor(read_func, sensor_name: str, default_value=None):
    """
    Safely read sensor with error handling
    
    Args:
        read_func: Function to call for reading sensor
        sensor_name: Name of sensor (for logging)
        default_value: Value to return on error
    
    Returns:
        Sensor value or default_value on error
    """
    try:
        return read_func()
    except Exception as e:
        print(f"Error reading {sensor_name}: {e}")
        return default_value

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def format_sensor_data(data: Dict[str, Any]) -> str:
    """
    Format sensor data for display
    
    Args:
        data: Dictionary of sensor readings
    
    Returns:
        Formatted string
    """
    lines = []
    for key, value in data.items():
        if isinstance(value, float):
            lines.append(f"{key}: {value:.2f}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)
