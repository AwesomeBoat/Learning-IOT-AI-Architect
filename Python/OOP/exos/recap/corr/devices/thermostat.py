"""
Thermostat - Équipement de gestion de température.
Principe SOLID: Single Responsibility - Gère uniquement la température
Principe SOLID: Open/Closed - Étendue de IoTDevice sans modification
"""

from .base import IoTDevice
from config import TEMP_MIN, TEMP_MAX


class Thermostat(IoTDevice):
    """
    Gestion de la température du bâtiment.
    
    Responsabilités:
    - Gérer la température cible avec validation (10-30°C)
    - Gérer la température actuelle
    - Implémenter execute_diagnostics() pour le thermostat
    """
    
    def __init__(self, device_id: str, name: str, ip_address: str, firmware_version: str,
                 target_temp: float = 21.5, current_temp: float = 20.0):
        """
        Initialise un thermostat.
        
        Args:
            device_id: Identifiant unique
            name: Nom lisible
            ip_address: Adresse IP
            firmware_version: Version du firmware
            target_temp: Température cible initiale
            current_temp: Température actuelle initiale
            
        Raises:
            ValueError: Si target_temp est hors limites
        """
        super().__init__(device_id, name, ip_address, firmware_version)
        self._target_temp = target_temp  # Le setter valide
        self.current_temp = current_temp
    
    @property
    def target_temp(self) -> float:
        """Retourne la température cible."""
        return self._target_temp
    
    @target_temp.setter
    def target_temp(self, value: float) -> None:
        """
        Fixe la température cible avec validation.
        
        Args:
            value: Température cible (10-30°C)
            
        Raises:
            ValueError: Si value n'est pas entre TEMP_MIN et TEMP_MAX
        """
        if not isinstance(value, (int, float)) or value < TEMP_MIN or value > TEMP_MAX:
            raise ValueError(
                f"La température cible doit être entre {TEMP_MIN}°C et {TEMP_MAX}°C, reçu: {value}°C"
            )
        self._target_temp = float(value)
    
    def adjust_temperature(self, delta: float) -> None:
        """
        Ajuste la température cible par une variation (delta).
        
        Args:
            delta: Variation de température à appliquer
            
        Raises:
            ValueError: Si la nouvelle température serait hors limites
        """
        new_temp = self.target_temp + delta
        self.target_temp = new_temp  # Le setter valide
        print(f"✓ Température cible de '{self.name}' ajustée à {new_temp}°C")
    
    def execute_diagnostics(self) -> str:
        """
        Retourne le rapport de diagnostic pour le thermostat.
        
        Returns:
            str: Rapport formaté incluant température actuelle et cible
        """
        status = "🟢 En ligne" if self.is_online else "🔴 Hors ligne"
        diff = self.current_temp - self.target_temp
        diff_str = f"+{diff:.1f}°C" if diff > 0 else f"{diff:.1f}°C"
        
        return (
            f"[{self.device_id}] Thermostat '{self.name}' - {status} | "
            f"Temp actuelle: {self.current_temp}°C | Cible: {self.target_temp}°C "
            f"(écart: {diff_str})"
        )
