"""
============================================================================
 FIL ROUGE "Batiment intelligent du centre de formation" - ETAPE 7 / 7 (BONUS)
 Retained + Last Will and Testament (version MicroPython)
============================================================================

Circuit simple (DHT22 seul). On se concentre sur deux mecanismes MQTT qui
repondent a la meme question : "Comment savoir si un objet connecte est
toujours vivant ?"

1) RETAINED sur un topic de statut :
      formation/<PRENOM>/batiment/etage1/salle3/status
   A chaque connexion "propre", l'ESP32 publie "en-ligne" en retained.

2) LAST WILL AND TESTAMENT (LWT) : configure AVANT la connexion avec
   client.set_last_will(...). Si l'ESP32 se deconnecte de facon inattendue
   (crash, coupure reseau...), c'est le BROKER qui publie lui-meme
   "hors-ligne" (retained) a sa place.

Pour observer le LWT sur Wokwi : lancez la simulation, verifiez sur MQTTX
Web que le statut passe a "en-ligne", puis ARRETEZ BRUTALEMENT la
simulation (bouton Stop) et observez le topic de statut passer a
"hors-ligne" apres quelques dizaines de secondes (delai du "keep alive").

IMPORTANT : personnalisez PRENOM avant de lancer la simulation.

Fin du fil rouge ! Retour a la table des matieres et au README maitre pour
la suite du programme.
============================================================================
"""

import dht
from machine import Pin
import network
import time
from umqtt.simple import MQTTClient

PRENOM = "changez_moi"

SSID_WIFI = "Wokwi-GUEST"
MOT_DE_PASSE_WIFI = ""

ADRESSE_BROKER = "test.mosquitto.org"
PORT_BROKER = 1883

BROCHE_DHT22 = 4
capteur = dht.DHT22(Pin(BROCHE_DHT22))

RACINE = "formation/{}/batiment/etage1/salle3/".format(PRENOM)
TOPIC_TEMPERATURE = RACINE + "capteur/temperature"
TOPIC_STATUS = RACINE + "status"

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
    # Le LWT DOIT etre configure avant connect() : c'est le message que le
    # broker publiera lui-meme si cet objet se deconnecte sans prevenir.
    client.set_last_will(TOPIC_STATUS, "hors-ligne", retain=True, qos=1)

    while True:
        try:
            client.connect()
            # Connexion "propre" -> on publie nous-memes le statut "en-ligne",
            # egalement en retained.
            client.publish(TOPIC_STATUS, "en-ligne", retain=True)
            print("Connecte au broker MQTT. Statut publie (retained) : en-ligne sur", TOPIC_STATUS)
            return client
        except OSError as erreur:
            print("Echec connexion MQTT ({}), nouvel essai dans 2s".format(erreur))
            time.sleep(2)


print()
print("=== Fil rouge - Etape 7/7 BONUS (MicroPython) : retained + LWT ===")
print("Topic de statut (avec LWT) :", TOPIC_STATUS)

connecter_wifi()
client_mqtt = connecter_mqtt()

while True:
    try:
        capteur.measure()
        temperature = capteur.temperature()
        payload = "{:.1f}".format(temperature)
        client_mqtt.publish(TOPIC_TEMPERATURE, payload)
        print("----------------------------------------------------")
        print("Temperature publiee :", payload, "C  (statut toujours 'en-ligne' en retained)")
    except OSError as erreur:
        print("Erreur MQTT/DHT22 ({}), reconnexion...".format(erreur))
        client_mqtt = connecter_mqtt()

    time.sleep(INTERVALLE_PUBLICATION_S)
