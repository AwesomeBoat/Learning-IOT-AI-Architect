"""
Menus interactifs pour chaque type d'équipement.
Principe SOLID: Single Responsibility - Chaque classe gère l'interaction pour un type d'équipement
Principe SOLID: Open/Closed - Facile d'ajouter de nouveaux menus sans modifier les existants
"""

from typing import Optional

from devices.smart_light import SmartLight
from devices.thermostat import Thermostat
from devices.security_camera import SecurityCamera


class SmartLightMenu:
    """Menu d'interaction pour une lampe connectée."""
    
    @staticmethod
    def show(light: SmartLight) -> None:
        """
        Affiche le menu et gère les options pour une SmartLight.
        
        Args:
            light: Objet SmartLight à contrôler
        """
        while True:
            print("\n--- Options SmartLight ---")
            print("1. Ajuster la luminosité")
            print("2. Changer la couleur")
            print("3. Retour")
            
            choice = input("Choix: ").strip()
            
            if choice == "1":
                try:
                    level = int(input("Luminosité (0-100): "))
                    light.set_brightness(level)
                except ValueError as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "2":
                color = input("Couleur (ex: Warm White, Cool White): ").strip()
                if color:
                    light.color = color
                    print(f"✓ Couleur changée à: {color}")
                else:
                    print("✗ Couleur vide, non modifiée")
            
            elif choice == "3":
                break
            
            else:
                print("✗ Choix invalide")


class ThermostatMenu:
    """Menu d'interaction pour un thermostat."""
    
    @staticmethod
    def show(thermostat: Thermostat) -> None:
        """
        Affiche le menu et gère les options pour un Thermostat.
        
        Args:
            thermostat: Objet Thermostat à contrôler
        """
        while True:
            print("\n--- Options Thermostat ---")
            print(f"Température cible actuelle: {thermostat.target_temp}°C")
            print(f"Température actuelle: {thermostat.current_temp}°C")
            print("1. Augmenter la température")
            print("2. Diminuer la température")
            print("3. Retour")
            
            choice = input("Choix: ").strip()
            
            if choice == "1":
                try:
                    delta = float(input("Augmenter de combien de degrés: "))
                    thermostat.adjust_temperature(delta)
                except ValueError as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "2":
                try:
                    delta = float(input("Diminuer de combien de degrés: "))
                    thermostat.adjust_temperature(-delta)
                except ValueError as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "3":
                break
            
            else:
                print("✗ Choix invalide")


class SecurityCameraMenu:
    """Menu d'interaction pour une caméra de surveillance."""
    
    @staticmethod
    def show(camera: SecurityCamera) -> None:
        """
        Affiche le menu et gère les options pour une SecurityCamera.
        
        Args:
            camera: Objet SecurityCamera à contrôler
        """
        while True:
            print("\n--- Options SecurityCamera ---")
            recording_status = "ACTIVE" if camera.is_recording else "INACTIVE"
            print(f"État enregistrement: {recording_status}")
            print("1. Basculer l'enregistrement")
            print("2. Retour")
            
            choice = input("Choix: ").strip()
            
            if choice == "1":
                camera.toggle_recording()
            
            elif choice == "2":
                break
            
            else:
                print("✗ Choix invalide")
