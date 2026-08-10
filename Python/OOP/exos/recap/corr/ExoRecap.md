# Exercice récapitulatif POO : Dashboard de Gestion IoT (CLI)

## 🏢 Contexte

Vous développez l'application console centrale pour piloter le réseau d'objets connectés d'un bâtiment intelligent. L'application doit permettre d'interagir avec différents équipements via un menu textuel interactif.

## 1. Modélisation des Équipements (`IoTDevice`)

Créer une classe de base `IoTDevice` et trois classes filles spécifiques :

- `SmartLight` (Éclairage connecté)
    
- `Thermostat` (Gestion de la température)
    
- `SecurityCamera` (Caméra de surveillance)
    

### 📌 Propriétés communes (`IoTDevice`)

- `device_id` (chaîne unique, ex: `"LIGHT_01"`)
    
- `name` (nom lisible, ex: `"Lumière Salon"`)
    
- `ip_address` (ex: `"192.168.1.45"`)
    
- `is_online` (booléen, `True` par défaut)
    
- `firmware_version` (ex: `"1.0.4"`)
    

### 📌 Spécificités des sous-classes (Héritage & Attributs propres)

- **`SmartLight` :**
    
    - `brightness` (int, de 0 à 100%)
        
    - `color` (string, ex: `"Warm White"`)
        
- **`Thermostat` :**
    
    - `target_temp` (float, ex: `21.5`)
        
    - `current_temp` (float, relevé instantané)
        
- **`SecurityCamera` :**
    
    - `is_recording` (booléen)
        
    - `storage_used_mb` (float, Mo consommés)
        

## 2. Comportements & POO (Encapsulation et Polymorphisme)

### A. Encapsulation

- Protéger la luminosité de `SmartLight` (`brightness`) : elle **doit être comprise strictemenent entre 0 et 100**. Utiliser un `@property` / _setter_ pour lever une erreur ou bloquer la valeur si elle dépasse.
    
- Protéger `target_temp` du `Thermostat` (ex: entre 10°C et 30°C).
    

### B. Polymorphisme (`execute_diagnostics()`)

Chaque classe possède une méthode `execute_diagnostics()` qui renvoie un rapport d'état sous forme de chaîne de caractères :

- `SmartLight` : Indique si elle est en ligne, sa luminosité et sa couleur.
    
- `Thermostat` : Indique la température actuelle par rapport à la température cible.
    
- `SecurityCamera` : Indique l'espace de stockage restant et si l'enregistrement est actif.
    

### C. Méthode d'action spécifique

Chaque équipement a une méthode d'action propre :

- `SmartLight.set_brightness(level)`
    
- `Thermostat.adjust_temperature(delta)`
    
- `SecurityCamera.toggle_recording()`
    

## 3. Le Gestionnaire de Réseau (`NetworkManager`)

Créer une classe `NetworkManager` qui orchestre l'ensemble de la flotte :

- **Attribut :** `devices` (un dictionnaire ou une liste d'objets `IoTDevice`).
    
- **Méthodes :**
    
    - `add_device(device)` : Ajoute un équipement au réseau.
        
    - `remove_device(device_id)` : Supprime un équipement par son ID.
        
    - `get_device(device_id)` : Recherche et renvoie l'objet équipement correspondant.
        
    - `ping_all()` : Parcourt la liste des appareils et met à jour leur statut `is_online` (de manière aléatoire pour simuler des pannes).
        
    - `run_global_diagnostics()` : **(Polymorphisme)** Appelle `execute_diagnostics()` sur tous les équipements enregistrés et affiche le rapport global dans la console.
        

## 4. L'Application & le Menu Interactif (CLI)

À l'exécution du script, l'application instancie un `NetworkManager` avec 3 ou 4 appareils pré-chargés, puis affiche un menu en boucle :

Plaintext

```
=== DASHBOARD IOT - SMART BUILDING ===
1. Lister tous les équipements (Statut & Diagnostics)
2. Interagir avec un équipement
3. Ajouter un nouvel équipement
4. Lancer un PING global sur le réseau
5. Quitter
> Choix : 
```

- **Si l'utilisateur choisit 2 :** L'app demande le `device_id`. Une fois l'objet trouvé, elle affiche les options spécifiques à son type (ex: ajuster la luminosité si c'est une lumière, modifier la température si c'est un thermostat).