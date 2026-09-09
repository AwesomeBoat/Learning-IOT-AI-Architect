"""
============================================================================
 FIL ROUGE "Batiment intelligent du centre de formation" - ETAPE 6 / 7
 Un actionneur pilote a distance (version MicroPython)
============================================================================

On se concentre sur l'ACTIONNEUR : la LED (eclairage) et le PIR (presence).
Deux logiques coexistent :

  1) Logique LOCALE (comme depuis l'etape 2) : la LED s'allume si une
     presence est detectee (on simplifie ici : plus de LDR).

  2) Logique A DISTANCE (nouveaute) : l'ESP32 est ABONNE (subscribe) au
     topic de commande suivant :

         formation/<PRENOM>/batiment/etage1/salle3/actionneur/eclairage/commande

     Un message "ON" force l'allumage, "OFF" force l'extinction, "AUTO"
     repasse en mode automatique (pilote par le PIR).

Cote etat, l'ESP32 PUBLIE l'etat courant de la LED, en RETAINED, sur :

    formation/<PRENOM>/batiment/etage1/salle3/actionneur/eclairage/etat

Le flag "retained" permet a un nouvel abonne qui se connecte APRES la
publication de recevoir immediatement le dernier etat connu.

En MicroPython, on utilise client.set_callback(...) pour reagir aux
messages recus, client.subscribe(...) pour s'abonner, et
client.check_msg() (non bloquant) dans la boucle pour verifier s'il y a un
message en attente, sans jamais bloquer la lecture du PIR.

IMPORTANT : personnalisez PRENOM avant de lancer la simulation.

Prochaine etape (7/7, bonus) : on approfondit "retained" et on ajoute un
Last Will and Testament (LWT).
============================================================================
"""

from machine import Pin
import network
import time
from umqtt.simple import MQTTClient

PRENOM = "changez_moi"

SSID_WIFI = "Wokwi-GUEST"
MOT_DE_PASSE_WIFI = ""

ADRESSE_BROKER = "test.mosquitto.org"
PORT_BROKER = 1883

BROCHE_PIR = 2
BROCHE_LED = 5

pir = Pin(BROCHE_PIR, Pin.IN)
led = Pin(BROCHE_LED, Pin.OUT)

RACINE = "formation/{}/batiment/etage1/salle3/actionneur/eclairage/".format(PRENOM)
TOPIC_COMMANDE = RACINE + "commande"
TOPIC_ETAT = RACINE + "etat"

# Mode courant : "AUTO" (pilote par le PIR), "ON" ou "OFF" (force via MQTT)
mode_courant = "AUTO"
dernier_etat_publie = None


def sur_message_recu(topic, message):
    global mode_courant
    texte = message.decode()
    print("Message recu sur '{}' : {}".format(topic.decode(), texte))
    if texte in ("ON", "OFF", "AUTO"):
        mode_courant = texte
    else:
        print("  (commande non reconnue, valeurs attendues : ON / OFF / AUTO)")


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
    client.set_callback(sur_message_recu)
    while True:
        try:
            client.connect()
            client.subscribe(TOPIC_COMMANDE)
            print("Connecte au broker MQTT, abonne a", TOPIC_COMMANDE)
            return client
        except OSError as erreur:
            print("Echec connexion MQTT ({}), nouvel essai dans 2s".format(erreur))
            time.sleep(2)


def publier_etat(client, allume):
    global dernier_etat_publie
    if allume == dernier_etat_publie:
        return
    client.publish(TOPIC_ETAT, "ON" if allume else "OFF", retain=True)
    dernier_etat_publie = allume
    print("  -> Publication (retained) sur {} = {}".format(TOPIC_ETAT, "ON" if allume else "OFF"))


print()
print("=== Fil rouge - Etape 6/7 (MicroPython) : actionneur pilote a distance ===")

connecter_wifi()
client_mqtt = connecter_mqtt()

while True:
    try:
        client_mqtt.check_msg()  # verifie si une commande MQTT est arrivee (non bloquant)
    except OSError as erreur:
        print("Connexion MQTT perdue ({}), reconnexion...".format(erreur))
        client_mqtt = connecter_mqtt()

    presence = pir.value()

    if mode_courant == "ON":
        eclairage_allume = True
    elif mode_courant == "OFF":
        eclairage_allume = False
    else:  # AUTO
        eclairage_allume = (presence == 1)

    led.value(1 if eclairage_allume else 0)

    try:
        publier_etat(client_mqtt, eclairage_allume)
    except OSError as erreur:
        print("Erreur de publication ({}), reconnexion...".format(erreur))
        client_mqtt = connecter_mqtt()

    time.sleep_ms(200)  # petite pause pour ne pas saturer la boucle
