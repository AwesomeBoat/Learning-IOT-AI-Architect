# IoT Dashboard - Smart Building

Application Python professionnelle de gestion d'objets connectés avec une architecture modulaire respectant les principes SOLID.

## 📋 Architecture & Structure

```
ExoRecapIOT/
├── main.py                 # Point d'entrée de l'application
├── config.py              # Configuration centralisée (constantes, appareils démo)
│
├── devices/               # Package des équipements IoT
│   ├── __init__.py
│   ├── base.py            # Classe abstraite IoTDevice (Single Responsibility)
│   ├── smart_light.py     # Implémentation SmartLight
│   ├── thermostat.py      # Implémentation Thermostat
│   └── security_camera.py # Implémentation SecurityCamera
│
├── network/               # Package de gestion réseau
│   ├── __init__.py
│   └── manager.py         # Classe NetworkManager (Dependency Inversion)
│
├── ui/                    # Package interface utilisateur
│   ├── __init__.py
│   ├── cli.py             # Classe IoTDashboardCLI (Single Responsibility)
│   └── menus.py           # Menus spécifiques par type d'équipement (Open/Closed)
│
└── utils/                 # Package utilitaires (pour futures extensions)
    └── __init__.py
```

## 🎯 Principes SOLID Respectés

### 1. **Single Responsibility Principle (SRP)**
- `IoTDevice` : Classe de base avec interface commune
- `SmartLight`, `Thermostat`, `SecurityCamera` : Chaque classe gère son type spécifique
- `NetworkManager` : Gère uniquement le réseau
- `IoTDashboardCLI` : Gère uniquement l'interface utilisateur
- `SmartLightMenu`, `ThermostatMenu`, `SecurityCameraMenu` : Chaque menu pour un type

### 2. **Open/Closed Principle (OCP)**
- Facile d'ajouter de nouveaux types d'équipements sans modifier les classes existantes
- Facile d'ajouter de nouveaux menus sans modifier le CLI existant
- Configuration externalisée dans `config.py`

### 3. **Liskov Substitution Principle (LSP)**
- Toutes les sous-classes (SmartLight, Thermostat, SecurityCamera) respectent le contrat de `IoTDevice`
- Polymorphisme `execute_diagnostics()` : chaque sous-classe implémente son diagnostic spécifique
- NetworkManager peut manipuler n'importe quel IoTDevice via l'interface commune

### 4. **Interface Segregation Principle (ISP)**
- `IoTDevice` : Interface minimale et cohérente
- Chaque équipement n'expose que les méthodes pertinentes
- Menus séparatisés par type pour éviter des options inutiles

### 5. **Dependency Inversion Principle (DIP)**
- `IoTDashboardCLI` dépend de `NetworkManager` (injecté en dépendance)
- `NetworkManager` dépend de l'abstraction `IoTDevice` (pas des implémentations concrètes)
- Facile de remplacer les implémentations sans modifier le code client

## 🚀 Démarrage Rapide

```bash
python main.py
```

## 📦 Fonctionnalités

### Équipements Supportés
1. **SmartLight** - Éclairage connecté
   - Contrôle de luminosité (0-100%)
   - Changement de couleur
   
2. **Thermostat** - Gestion de température
   - Température cible (10-30°C)
   - Ajustement par variation (delta)
   
3. **SecurityCamera** - Caméra de surveillance
   - Toggle enregistrement
   - Gestion du stockage

### Menu Principal
1. Lister tous les équipements avec diagnostics
2. Interagir avec un équipement (sous-menu spécifique)
3. Ajouter un nouvel équipement
4. Lancer un PING global (simulation statuts aléatoires)
5. Quitter

## 🔒 Encapsulation

- **SmartLight.brightness** : Property/setter avec validation stricte (0-100)
- **Thermostat.target_temp** : Property/setter avec validation stricte (10-30°C)
- Erreurs levées si dépassement des limites

## 🔌 Polymorphisme

Chaque équipement implémente `execute_diagnostics()` retournant un rapport adapté :
- SmartLight : Luminosité + Couleur
- Thermostat : Température actuelle vs cible
- SecurityCamera : État enregistrement + Stockage utilisé

## 🎓 Concepts POO Démontrés

- ✅ Héritage (SmartLight, Thermostat, SecurityCamera héritent de IoTDevice)
- ✅ Polymorphisme (execute_diagnostics() polymorphe)
- ✅ Encapsulation (properties avec setters validants)
- ✅ Abstraction (classe de base abstraite IoTDevice)
- ✅ Composition (NetworkManager compose une collection d'IoTDevice)

## 📝 Exemples d'Utilisation

### Créer un nouvel équipement
```python
light = SmartLight(
    device_id="LIGHT_03",
    name="Lumière Chambre",
    ip_address="192.168.1.47",
    firmware_version="1.0.4",
    brightness=50,
    color="Cool White"
)

network.add_device(light)
```

### Modifier la luminosité (avec validation)
```python
try:
    light.set_brightness(75)  # ✓ OK
    light.set_brightness(150) # ✗ ValueError levée
except ValueError as e:
    print(f"Erreur: {e}")
```

### Ajuster la température
```python
try:
    thermostat.adjust_temperature(+1.5)  # Augmenter de 1.5°C
    thermostat.adjust_temperature(-2.0)  # Diminuer de 2°C
except ValueError as e:
    print(f"Erreur: {e}")
```

## 🧪 Testing

L'application inclut 4 appareils de démo :
- 2 SmartLights (Salon, Cuisine)
- 1 Thermostat (Étage 1)
- 1 SecurityCamera (Entrée)

Testable sans modification du code !
