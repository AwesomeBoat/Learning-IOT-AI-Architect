"""
Configuration centralisée de l'application IoT Dashboard.
Principe SOLID: Configuration isolée pour éviter les magic strings et constantes dispersées.
"""

# Limites de température (Thermostat)
TEMP_MIN = 10.0
TEMP_MAX = 30.0

# Limites de luminosité (SmartLight)
BRIGHTNESS_MIN = 0
BRIGHTNESS_MAX = 100

# Stockage (SecurityCamera)
STORAGE_TOTAL_MB = 2048.0

# Simulation réseau
PING_ONLINE_PROBABILITY = 0.85  # 85% de chance d'être en ligne

# Appareils pré-chargés
DEMO_DEVICES = [
    {
        "type": "SmartLight",
        "device_id": "LIGHT_01",
        "name": "Lumière Salon",
        "ip_address": "192.168.1.45",
        "firmware_version": "1.0.4",
        "brightness": 75,
        "color": "Warm White"
    },
    {
        "type": "SmartLight",
        "device_id": "LIGHT_02",
        "name": "Lumière Cuisine",
        "ip_address": "192.168.1.46",
        "firmware_version": "1.0.4",
        "brightness": 50,
        "color": "Cool White"
    },
    {
        "type": "Thermostat",
        "device_id": "THERMO_01",
        "name": "Thermostat Étage 1",
        "ip_address": "192.168.1.50",
        "firmware_version": "2.1.0",
        "target_temp": 21.5,
        "current_temp": 20.2
    },
    {
        "type": "SecurityCamera",
        "device_id": "CAM_01",
        "name": "Caméra Entrée",
        "ip_address": "192.168.1.60",
        "firmware_version": "1.5.2",
        "is_recording": False,
        "storage_used_mb": 512.5
    }
]
