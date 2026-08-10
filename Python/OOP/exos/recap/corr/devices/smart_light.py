"""
SmartLight - Équipement d'éclairage connecté.
Principe SOLID: Single Responsibility - Gère uniquement l'éclairage
Principe SOLID: Open/Closed - Étendue de IoTDevice sans modification
"""

from .base import IoTDevice
from config import BRIGHTNESS_MIN, BRIGHTNESS_MAX


class SmartLight(IoTDevice):
    """
    Éclairage connecté avec contrôle de luminosité et couleur.
    
    Responsabilités:
    - Gérer la luminosité avec validation (0-100%)
    - Gérer la couleur
    - Implémenter execute_diagnostics() pour l'éclairage
    """
    
    def __init__(self, device_id: str, name: str, ip_address: str, firmware_version: str,
                 brightness: int = 50, color: str = "Warm White"):
        """
        Initialise une lampe connectée.
        
        Args:
            device_id: Identifiant unique
            name: Nom lisible
            ip_address: Adresse IP
            firmware_version: Version du firmware
            brightness: Luminosité initiale (0-100)
            color: Couleur initiale
            
        Raises:
            ValueError: Si brightness est hors limites
        """
        super().__init__(device_id, name, ip_address, firmware_version)
        self._brightness = brightness  # Utilise _brightness car le setter le validera
        self.color = color
    
    @property
    def brightness(self) -> int:
        """Retourne la luminosité actuelle."""
        return self._brightness
    
    @brightness.setter
    def brightness(self, value: int) -> None:
        """
        Fixe la luminosité avec validation.
        
        Args:
            value: Niveau de luminosité (0-100)
            
        Raises:
            ValueError: Si value n'est pas entre 0 et 100
        """
        if not isinstance(value, (int, float)) or value < BRIGHTNESS_MIN or value > BRIGHTNESS_MAX:
            raise ValueError(
                f"La luminosité doit être entre {BRIGHTNESS_MIN} et {BRIGHTNESS_MAX}, reçu: {value}"
            )
        self._brightness = int(value)
    
    def set_brightness(self, level: int) -> None:
        """
        Ajuste la luminosité de la lampe.
        
        Args:
            level: Niveau de luminosité (0-100)
            
        Raises:
            ValueError: Si level est hors limites
        """
        self.brightness = level  # Le setter valide
        print(f"✓ Luminosité de '{self.name}' ajustée à {level}%")
    
    def execute_diagnostics(self) -> str:
        """
        Retourne le rapport de diagnostic pour la lampe.
        
        Returns:
            str: Rapport formaté incluant statut, luminosité et couleur
        """
        status = "🟢 En ligne" if self.is_online else "🔴 Hors ligne"
        return (
            f"[{self.device_id}] SmartLight '{self.name}' - {status} | "
            f"Luminosité: {self.brightness}% | Couleur: {self.color}"
        )
