from classes.network_manager import NetworkManager
from classes.security_camera import SecurityCamera
from classes.smart_light import SmartLight
from classes.thermostat import Thermostat
import time


def add_new_device(home_network):
    new_device_id =  input("Id of device: ")
    new_device_name = input("Name of device: ")
    new_device_ip = input("IP of device: ")
    new_device_version = input("Firmware version: ")
    print("""
    ===SELECT DEVICE TYPE===
        Light : 1
        Thermo : 2
        Camera : 3

    """)

    type_of_device = int(input())

    match type_of_device :
        case 1:
            new_device_brightness = int(input("Enter the brightness of new device"))
            new_device_color = input("Enter color of device")
            SmartLight(new_device_id, new_device_name, new_device_ip, False, new_device_version, new_device_brightness, new_device_color)
            home_network.add_device(new_device)

        case 2:
            new_device_target_temp = float(input("Enter the target temp"))
            new_device = Thermostat(new_device_id, new_device_name, new_device_ip, False, new_device_version,new_device_target_temp)
            home_network.add_device(new_device)

    
        case 3:
            new_device_is_recording = False
            new_device_storage = int(input("Enter the storage in mb: "))
            new_device = SecurityCamera(new_device_id,new_device_name,new_device_ip, False, new_device_version, new_device_is_recording, new_device_storage)
            home_network.add_device(new_device)
    

def interact_with_device(network_manager):
    device_id = input("Enter the device Id : ")
    try:
        device = network_manager.get_device(device_id)
    except:
        pass
    device_class = device.__class__.__name__

    # Interact with SmartLight
    if device_class == "SmartLight": 
        print(f"""
        === {device_id} ===
        1. Ajuster la luminosité
        2. retour
        """)
        choice = int(input("> Choix : "))
        match choice:
            case 1:
                brightness = input('Entrez la valeur de la luminosité, min. 0 | max. 100')
                device.set_brightness(brightness)
            case 2:
                pass



    # Interact with Thermostat
    elif device_class == "Thermostat": 
        print(f"""
        === {device_id} ===
        1. Ajuster la température
        2. retour
        """)
        choice = int(input("> Choix : "))
        match choice:
            case 1: 
                delta = input("Entrez le delta pour ajuster la température, Ex. 2 | -3 : ")
                device.adjust_temperature(delta)
            case 2:
                pass

    # Interact with Cameras
    elif device_class == "SecurityCamera": 
        print(f"""
        === {device_id} ===
        1. retour
        """)
        choice = int(input("> Choix : "))
        match choice:
            case 1:
                pass

    


def main_loop_cli(network_manager):
    running = True
    while running:
        print("""
        === DASHBOARD IOT - SMART BUILDING ===
        1. Lister tous les équipements (Statut & Diagnostics)
        2. Interagir avec un équipement
        3. Ajouter un nouvel équipement
        4. Lancer un PING global sur le réseau
        5. Quitter
        """)
        user_choice = int(input("> Choix : "))

        match user_choice:
            case 1:
                network_manager.run_global_diagnostics()
                time.sleep(4)
            case 2:
                interact_with_device(network_manager)
                time.sleep(4)
            case 3:
                device_to_add = add_new_device(home_network=home_network)
                network_manager.add_device(device_to_add)
                time.sleep(4)
            case 4:
                network_manager.ping_all()
                time.sleep(4)
            case 5:
                print("Goodbye.")
                running = False 
            




if __name__ == "__main__":


    # Create Devices

    light1 = SmartLight("LIGHT01","Lumiere Salon", "127.0.0.1", True, "1.5", 0, "white")
    light2 = SmartLight("LIGHT02","Lumiere Cuisine", "127.0.0.1", False, "1.5", 0, "white")
    light3 = SmartLight("LIGHT03","Lumiere Chambre", "127.0.0.1", True, "1.5", 100, "red")
    light4 = SmartLight("LIGHT04","Lumiere Salle de Jeux", "127.0.0.1", True, "1.5", 50, "blue")


    thermo1 = Thermostat("THERMO01","Thermostat rez-de-chaussé","127.0.0.2",True,"0.5",22.5)
    thermo2 = Thermostat("THERMO02","Thermostat 1er Etage","127.0.0.2",False,"0.5",18)


    cam1 = SecurityCamera("CAM01","Caméra Jardin","127.0.0.3",True,"12.5.6", True, 250)
    cam2 = SecurityCamera("CAM02", "Caméra Garage", "127.0.0.4", False, "12.5.6",False,250)
    cam3 = SecurityCamera("CAM03", "Caméra Hall", "127.0.0.5", True, "12.5.6",False,250)

    # Create Manager
    home_network = NetworkManager()

    # Add devices
    dev_list = [light1,light2,light3,light4,thermo1,thermo2,cam1,cam2,cam3]

    for device in dev_list:
        home_network.add_device(device)


    main_loop_cli(home_network)


