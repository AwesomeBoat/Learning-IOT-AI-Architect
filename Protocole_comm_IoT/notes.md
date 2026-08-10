# Protocoles de Communications IoT

## Rappel réseau

### TCP

- Etablissement d'une connexion avant tout envois de données
- accusé de reception pour chaque paquet
    
Overhead : elevé
Fiabilitié : garantie
usage IoT : MQTT


### UDP

- Envoie directement les données sans connexion sans garantie de réception ni ordre d'arrivée

Overhead : minimal
Fiabilitié : aucune garantie
usage IoT : CoAP


MQTT => fiable, adapté aux données critiques;
CoAP => ultra-léger ...


## Grille de critère choix de protocole

1. Portée :
    - BLE qlq metres
    - Wi-Fi-MQTT = Bâtiment
    - LoRaWAN = plusieurs km (champ ville)

2. Énergie
    - LoRaWAN : années sur pile
    - ESP32 Wi-Fi : quelques heures

3. Bande passante
    -Envoyer quelques octes VS millions d'octet

4. Topologie
    - Point à Point 
    - Etoile
    - Many to Many via broker (pub/sub MQTT)

5. Latence
    - Alarme incendie (basse) VS relevé météo (ok un peu plus longue)

6. Coût
    - Abonnement réseau (LoRaWAN)
    - Matériel (module radio)
    - Licence logicielle (broker cloud)


## MQTT
protocole de messagerie léger conçu pour essayer de consommer le moins possible (peu de RAM, énergie) sur des réseaux peu fiables - Fonctionne sur TCP

- l'en-tête MQTT ne fait que 2 octets

### Modèle MQTT

Modèle Publish / Subscribe

on a un broker (dispatcher / hub) 

tous les appareils publient sur les topics. le broker se charge de router les informations 

Publish => un objet envoie un message sans savoir qui le lis.

Subscribe => (le Broker consomme la ressource, pas le capteur abonné)

Le rôle du broker MQTT => 


### Utilisation 