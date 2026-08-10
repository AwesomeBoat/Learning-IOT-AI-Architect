"""
Interface CLI de l'application IoT Dashboard.
Principe SOLID: Single Responsibility - Gère uniquement l'interface utilisateur
Principe SOLID: Dependency Inversion - Utilise NetworkManager comme dépendance injectée
"""

from typing import Optional

from network.manager import NetworkManager
from devices.smart_light import SmartLight
from devices.thermostat import Thermostat
from devices.security_camera import SecurityCamera
from ui.menus import SmartLightMenu, ThermostatMenu, SecurityCameraMenu
from config import TEMP_MIN, TEMP_MAX, BRIGHTNESS_MIN, BRIGHTNESS_MAX


class IoTDashboardCLI:
    """
    Interface CLI principale pour gérer le réseau IoT.
    
    Responsabilités:
    - Afficher le menu principal
    - Gérer les interactions utilisateur
    - Orchestrer les opérations via NetworkManager
    - Déléguer les contrôles spécifiques aux menus de chaque type
    """
    
    def __init__(self, network_manager: NetworkManager):
        """
        Initialise le CLI avec un gestionnaire réseau.
        
        Args:
            network_manager: Instance de NetworkManager pour orchestrer les opérations
        """
        self.network = network_manager
    
    def display_header(self) -> None:
        """Affiche le header de l'application."""
        print("\n" + "="*80)
        print("🏢 DASHBOARD IoT - SMART BUILDING")
        print("="*80 + "\n")
    
    def display_main_menu(self) -> None:
        """Affiche le menu principal."""
        print("\n--- MENU PRINCIPAL ---")
        print("1. Lister tous les équipements (Statut & Diagnostics)")
        print("2. Interagir avec un équipement")
        print("3. Ajouter un nouvel équipement")
        print("4. Lancer un PING global sur le réseau")
        print("5. Quitter")
    
    def interact_with_device(self, device_id: str) -> None:
        """
        Gère l'interaction avec un équipement spécifique.
        Utilise le polymorphisme pour déléguer au bon menu.
        
        Args:
            device_id: ID de l'équipement à contrôler
        """
        device = self.network.get_device(device_id)
        
        if device is None:
            print(f"✗ Équipement '{device_id}' non trouvé\n")
            return
        
        print(f"\n🔧 Interaction avec: {device}")
        
        # Polymorphisme : délégue au menu approprié selon le type
        if isinstance(device, SmartLight):
            SmartLightMenu.show(device)
        elif isinstance(device, Thermostat):
            ThermostatMenu.show(device)
        elif isinstance(device, SecurityCamera):
            SecurityCameraMenu.show(device)
        else:
            print("✗ Type d'équipement non supporté")
    
    def add_device_interactive(self) -> None:
        """Interface interactive pour ajouter un nouvel équipement."""
        print("\n🆕 Ajouter un nouvel équipement")
        print("Type d'équipement:")
        print("1. SmartLight")
        print("2. Thermostat")
        print("3. SecurityCamera")
        
        choice = input("Choix: ").strip()
        
        if choice not in ["1", "2", "3"]:
            print("✗ Choix invalide")
            return
        
        # Données communes
        device_id = input("ID de l'équipement (ex: LIGHT_03): ").strip()
        
        if not device_id:
            print("✗ ID vide, annulation")
            return
        
        if device_id in self.network.devices:
            print(f"✗ Un équipement avec l'ID '{device_id}' existe déjà")
            return
        
        name = input("Nom de l'équipement: ").strip()
        ip = input("Adresse IP: ").strip()
        firmware = input("Version firmware: ").strip()
        
        try:
            if choice == "1":
                brightness = int(input(f"Luminosité initiale ({BRIGHTNESS_MIN}-{BRIGHTNESS_MAX}): "))
                color = input("Couleur: ").strip()
                device = SmartLight(device_id, name, ip, firmware, brightness, color)
            
            elif choice == "2":
                target_temp = float(input(f"Température cible ({TEMP_MIN}-{TEMP_MAX}): "))
                current_temp = float(input("Température actuelle: "))
                device = Thermostat(device_id, name, ip, firmware, target_temp, current_temp)
            
            else:  # choice == "3"
                is_recording = input("En enregistrement ? (o/n): ").strip().lower() == "o"
                storage = float(input("Espace utilisé (MB): "))
                device = SecurityCamera(device_id, name, ip, firmware, is_recording, storage)
            
            self.network.add_device(device)
        
        except ValueError as e:
            print(f"✗ Erreur de saisie: {e}")
    
    def run(self) -> None:
        """Boucle principale du menu."""
        self.display_header()
        
        while True:
            self.display_main_menu()
            
            choice = input("\n> Choix: ").strip()
            
            if choice == "1":
                self.network.list_all_devices()
                self.network.run_global_diagnostics()
            
            elif choice == "2":
                device_id = input("Entrez l'ID de l'équipement: ").strip()
                self.interact_with_device(device_id)
            
            elif choice == "3":
                self.add_device_interactive()
            
            elif choice == "4":
                self.network.ping_all()
            
            elif choice == "5":
                print("\n👋 Au revoir!\n")
                break
            
            else:
                print("✗ Choix invalide. Veuillez réessayer.")
