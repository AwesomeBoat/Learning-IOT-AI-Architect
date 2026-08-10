"""
Base abstraite pour tous les équipements IoT.
Principe SOLID: Single Responsibility - classe de base avec interface commune
Principe SOLID: Liskov Substitution - toutes les sous-classes respectent le contrat
"""

from abc import ABC, abstractmethod


class IoTDevice(ABC):
    """
    Classe abstraite de base pour tous les équipements IoT.
    
    Responsabilités:
    - Définir l'interface commune à tous les équipements
    - Gérer les propriétés communes (device_id, name, ip_address, etc.)
    - Enforcer l'implémentation de execute_diagnostics() dans les sous-classes
    """
    
    def __init__(self, device_id: str, name: str, ip_address: str, firmware_version: str):
        """
        Initialise un équipement IoT.
        
        Args:
            device_id: Identifiant unique (ex: "LIGHT_01")
            name: Nom lisible (ex: "Lumière Salon")
            ip_address: Adresse IP (ex: "192.168.1.45")
            firmware_version: Version du firmware (ex: "1.0.4")
        """
        self.device_id = device_id
        self.name = name
        self.ip_address = ip_address
        self.is_online = True
        self.firmware_version = firmware_version
    
    @abstractmethod
    def execute_diagnostics(self) -> str:
        """
        Retourne un rapport d'état spécifique à chaque équipement.
        
        Returns:
            str: Rapport de diagnostic formaté
        """
        pass
    
    def __str__(self) -> str:
        """Affichage texte de l'équipement."""
        status = "🟢 ONLINE" if self.is_online else "🔴 OFFLINE"
        return f"[{self.device_id}] {self.name} - {status} - IP: {self.ip_address}"
