"""
Point d'entrée de l'application IoT Dashboard.
Principe SOLID: Dependency Injection - Initialise les dépendances et les injecte
"""

from network.manager import NetworkManager
from devices.smart_light import SmartLight
from devices.thermostat import Thermostat
from devices.security_camera import SecurityCamera
from ui.cli import IoTDashboardCLI
from config import DEMO_DEVICES


def initialize_demo_devices(network: NetworkManager) -> None:
    """
    Pré-charge les équipements de démonstration.
    
    Args:
        network: Instance NetworkManager où ajouter les appareils
    """
    for device_config in DEMO_DEVICES:
        device_type = device_config.pop("type")
        
        if device_type == "SmartLight":
            device = SmartLight(**device_config)
        elif device_type == "Thermostat":
            device = Thermostat(**device_config)
        elif device_type == "SecurityCamera":
            device = SecurityCamera(**device_config)
        else:
            continue
        
        network.add_device(device)


def main() -> None:
    """Point d'entrée principal de l'application."""
    # Création des dépendances
    network_manager = NetworkManager()
    
    # Initialisation des appareils de démo
    initialize_demo_devices(network_manager)
    
    # Création et lancement du CLI
    dashboard = IoTDashboardCLI(network_manager)
    dashboard.run()


if __name__ == "__main__":
    main()
