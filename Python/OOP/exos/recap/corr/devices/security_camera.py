"""
SecurityCamera - Équipement de surveillance vidéo.
Principe SOLID: Single Responsibility - Gère uniquement la caméra
Principe SOLID: Open/Closed - Étendue de IoTDevice sans modification
"""

from .base import IoTDevice
from config import STORAGE_TOTAL_MB


class SecurityCamera(IoTDevice):
    """
    Caméra de surveillance avec enregistrement et gestion du stockage.
    
    Responsabilités:
    - Gérer l'état d'enregistrement
    - Gérer l'utilisation du stockage
    - Implémenter execute_diagnostics() pour la caméra
    """
    
    def __init__(self, device_id: str, name: str, ip_address: str, firmware_version: str,
                 is_recording: bool = False, storage_used_mb: float = 512.5):
        """
        Initialise une caméra de surveillance.
        
        Args:
            device_id: Identifiant unique
            name: Nom lisible
            ip_address: Adresse IP
            firmware_version: Version du firmware
            is_recording: État initial d'enregistrement
            storage_used_mb: Espace utilisé en MB
        """
        super().__init__(device_id, name, ip_address, firmware_version)
        self.is_recording = is_recording
        self.storage_used_mb = storage_used_mb
        self.storage_total_mb = STORAGE_TOTAL_MB
    
    def toggle_recording(self) -> None:
        """Active ou désactive l'enregistrement."""
        self.is_recording = not self.is_recording
        state = "ACTIVE" if self.is_recording else "INACTIVE"
        print(f"✓ Enregistrement de '{self.name}' maintenant {state}")
    
    def execute_diagnostics(self) -> str:
        """
        Retourne le rapport de diagnostic pour la caméra.
        
        Returns:
            str: Rapport formaté incluant statut, enregistrement et stockage
        """
        status = "🟢 En ligne" if self.is_online else "🔴 Hors ligne"
        recording_status = "🔴 Enregistrement" if self.is_recording else "⚪ Inactif"
        storage_remaining = self.storage_total_mb - self.storage_used_mb
        storage_percent = (self.storage_used_mb / self.storage_total_mb) * 100
        
        return (
            f"[{self.device_id}] Caméra '{self.name}' - {status} | "
            f"{recording_status} | Stockage: {storage_percent:.1f}% utilisé "
            f"({storage_remaining:.1f} MB restants)"
        )
