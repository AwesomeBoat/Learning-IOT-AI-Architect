"""Devices package - Définition de tous les types d'équipements IoT."""

from .base import IoTDevice
from .smart_light import SmartLight
from .thermostat import Thermostat
from .security_camera import SecurityCamera

__all__ = ["IoTDevice", "SmartLight", "Thermostat", "SecurityCamera"]
