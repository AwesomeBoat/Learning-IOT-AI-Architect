"""
============================================================================
 FIL ROUGE "Batiment intelligent du centre de formation" - ETAPE 5 / 7
 Arborescence multi-capteurs (version MicroPython)
============================================================================

Retour au circuit complet de la Salle 3 (DHT22 + PIR + LDR, sans la LED -
elle revient a l'etape 6 en tant qu'actionneur pilotable a distance).
Chaque grandeur mesuree a SON PROPRE topic, tous rattaches a la meme
racine :

    formation/<PRENOM>/batiment/etage1/salle3/capteur/temperature
    formation/<PRENOM>/batiment/etage1/salle3/capteur/humidite
    formation/<PRENOM>/batiment/etage1/salle3/capteur/presence
    formation/<PRENOM>/batiment/etage1/salle3/capteur/luminosite

IMPORTANT : personnalisez PRENOM avant de lancer la simulation.

Prochaine etape (6/7) : on ajoute un ACTIONNEUR (la LED) qu'on peut piloter
A DISTANCE via MQTT, en plus de son automatisation locale.
============================================================================
"""

import dht
from machine import Pin, ADC
import network
import time
from umqtt.simple import MQTTClient

PRENOM = "changez_moi"

SSID_WIFI = "Wokwi-GUEST"
MOT_DE_PASSE_WIFI = ""

ADRESSE_BROKER = "test.mosquitto.org"
PORT_BROKER = 1883

BROCHE_DHT22 = 4
BROCHE_PIR = 2
BROCHE_LDR = 34

capteur = dht.DHT22(Pin(BROCHE_DHT22))
pir = Pin(BROCHE_PIR, Pin.IN)
ldr = ADC(Pin(BROCHE_LDR))
ldr.atten(ADC.ATTN_11DB)

RACINE_TOPICS = "formation/{}/batiment/etage1/salle3/capteur/".format(PRENOM)
INTERVALLE_PUBLICATION_S = 5


def connecter_wifi():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print("Connexion au Wi-Fi '{}' ...".format(SSID_WIFI), end="")
        sta.connect(SSID_WIFI, MOT_DE_PASSE_WIFI)
        while not sta.isconnected():
            time.sleep_ms(250)
            print(".", end="")
    print(" connecte !")
    print("Adresse IP :", sta.ifconfig()[0])


def connecter_mqtt():
    client_id = "esp32-formation-{}".format(PRENOM)
    client = MQTTClient(client_id, ADRESSE_BROKER, port=PORT_BROKER)
    while True:
        try:
            client.connect()
            print("Connecte au broker MQTT", ADRESSE_BROKER)
            return client
        except OSError as erreur:
            print("Echec connexion MQTT ({}), nouvel essai dans 2s".format(erreur))
            time.sleep(2)


def publier_valeur(client, sous_topic, valeur):
    topic_complet = RACINE_TOPICS + sous_topic
    try:
        client.publish(topic_complet, str(valeur))
        print("  ->", topic_complet, "=", valeur, " [OK]")
    except OSError as erreur:
        print("  ->", topic_complet, "= ECHEC (", erreur, ")")
        raise


print()
print("=== Fil rouge - Etape 5/7 (MicroPython) : arborescence multi-capteurs ===")
print("Racine des topics :", RACINE_TOPICS)

connecter_wifi()
client_mqtt = connecter_mqtt()

while True:
    print("----------------------------------------------------")
    print("Publication de l'arborescence complete :")
    try:
        try:
            capteur.measure()
            publier_valeur(client_mqtt, "temperature", "{:.1f}".format(capteur.temperature()))
            publier_valeur(client_mqtt, "humidite", "{:.1f}".format(capteur.humidity()))
        except OSError:
            print("  -> lecture DHT22 invalide, capteur ignore ce cycle")

        presence = pir.value()
        publier_valeur(client_mqtt, "presence", "1" if presence == 1 else "0")

        luminosite = ldr.read()
        publier_valeur(client_mqtt, "luminosite", luminosite)

    except OSError as erreur:
        print("Erreur MQTT ({}), reconnexion...".format(erreur))
        client_mqtt = connecter_mqtt()

    time.sleep(INTERVALLE_PUBLICATION_S)
