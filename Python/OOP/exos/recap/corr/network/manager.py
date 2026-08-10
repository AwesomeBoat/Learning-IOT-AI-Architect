"""
NetworkManager - Gestionnaire de réseau IoT.
Principe SOLID: Single Responsibility - Gère le réseau d'équipements
Principe SOLID: Dependency Inversion - Dépend de l'abstraction IoTDevice
"""

import random
from typing import Dict, Optional

from devices.base import IoTDevice
from config import PING_ONLINE_PROBABILITY


class NetworkManager:
    """
    Orchestre l'ensemble de la flotte d'équipements IoT.
    
    Responsabilités:
    - Ajouter/Supprimer/Rechercher des équipements
    - Simuler des pings réseau
    - Afficher les diagnostics globaux
    - Maintenir un dictionnaire des appareils actifs
    """
    
    def __init__(self):
        """Initialise le gestionnaire de réseau avec un dictionnaire vide."""
        self.devices: Dict[str, IoTDevice] = {}
    
    def add_device(self, device: IoTDevice) -> None:
        """
        Ajoute un équipement au réseau.
        
        Args:
            device: Objet IoTDevice à ajouter
        """
        self.devices[device.device_id] = device
        print(f"✓ Équipement '{device.name}' ({device.device_id}) ajouté au réseau")
    
    def remove_device(self, device_id: str) -> None:
        """
        Supprime un équipement par son ID.
        
        Args:
            device_id: ID de l'équipement à supprimer
        """
        if device_id in self.devices:
            device_name = self.devices[device_id].name
            del self.devices[device_id]
            print(f"✓ Équipement '{device_name}' ({device_id}) supprimé du réseau")
        else:
            print(f"✗ Équipement '{device_id}' non trouvé")
    
    def get_device(self, device_id: str) -> Optional[IoTDevice]:
        """
        Recherche et retourne un équipement par son ID.
        
        Args:
            device_id: ID de l'équipement
            
        Returns:
            IoTDevice si trouvé, None sinon
        """
        return self.devices.get(device_id, None)
    
    def ping_all(self) -> None:
        """
        Parcourt tous les appareils et met à jour leur statut de connexion.
        Simule des pannes aléatoires basées sur PING_ONLINE_PROBABILITY.
        """
        print("\n📡 PING global en cours...")
        online_count = 0
        
        for device in self.devices.values():
            # Simulation : probabilité de chance que l'appareil soit en ligne
            device.is_online = random.random() > (1 - PING_ONLINE_PROBABILITY)
            status = "✓ En ligne" if device.is_online else "✗ Hors ligne"
            print(f"  {device.device_id}: {status}")
            if device.is_online:
                online_count += 1
        
        total = len(self.devices)
        print(f"\n📊 Résumé: {online_count}/{total} appareil(s) en ligne")
    
    def run_global_diagnostics(self) -> None:
        """
        Affiche le rapport de diagnostic pour tous les équipements.
        Démontre le polymorphisme : chaque type d'équipement retourne son diagnostic spécifique.
        """
        print("\n" + "="*80)
        print("🔍 RAPPORT DE DIAGNOSTIC GLOBAL - Tous les équipements")
        print("="*80)
        
        if not self.devices:
            print("Aucun équipement dans le réseau.")
            print("="*80 + "\n")
            return
        
        for device in self.devices.values():
            print(device.execute_diagnostics())
        
        print("="*80 + "\n")
    
    def list_all_devices(self) -> None:
        """Liste tous les équipements avec leur statut."""
        print("\n" + "="*80)
        print("📋 LISTE DE TOUS LES ÉQUIPEMENTS")
        print("="*80)
        
        if not self.devices:
            print("Aucun équipement dans le réseau.")
            print("="*80 + "\n")
            return
        
        for device in self.devices.values():
            print(device)
        
        print("="*80 + "\n")
    
    def get_device_count(self) -> int:
        """
        Retourne le nombre d'équipements dans le réseau.
        
        Returns:
            Nombre d'équipements
        """
        return len(self.devices)
    
    def get_online_count(self) -> int:
        """
        Retourne le nombre d'équipements en ligne.
        
        Returns:
            Nombre d'équipements en ligne
        """
        return sum(1 for device in self.devices.values() if device.is_online)
