import dht
import time
import math
from machine import Pin, ADC
import network
from umqtt.simple import MQTTClient

#Config des numéro de pin pour les branchements
BROCHE_DHT22 = 2
BROCHE_PIR = 13
BROCHE_LDR = 34
#création de l'objet contrôlant mon DHT22
capteur_temperature = dht.DHT22(Pin(BROCHE_DHT22))
#création de mon objet pour PIR
pir = Pin(BROCHE_PIR)
#création de l'objet pour le photo transistor
ldr = ADC(Pin(BROCHE_LDR))
 

#Variable
INTERVALLE_LECTURE_MS= 2000
derniere_lecture = 0
SEUIL_LUMINOSITE = 200

#infos wifi
SSID_WIFI = "Wokwi-GUEST"
MOT_DE_PASSE_WIFI=""

#infos pour topics
#MACHINE_NAME="NETLAB100"
ADRESSE_BROKER="test.mosquitto.org"
PORT_BROKER=1883
TOPIC_TEMPERATURE ="TechnoFutur/BESTIOTArchi/NETLAB100/Temperature"

#Methode de connexion au wifi
def connexion_wifi():
    sta = network.WLAN(network.STA_IF) #récupération de l'état de mon "wifi"
    sta.active(True)
    if not sta.isconnected():
        print (f'Connexion au wifi {SSID_WIFI}...')
        sta.connect(SSID_WIFI, MOT_DE_PASSE_WIFI)
        while not sta.isconnected():
            time.sleep_ms(250)
            print(".")
    print("Connecté")
    ipwifi = sta.ifconfig()[0]
    print(f'Adresse IP : {ipwifi}')
    return sta

#Methode de connexion MQTT
def connexion_mqtt():
    client_id="FormationIOT_NETLAB100"
    client= MQTTClient(client_id, ADRESSE_BROKER,port=PORT_BROKER)
    while True:
        try:
            client.connect()
            print("Connexion au broker MQTT")
            time.sleep(2)
            return client
        except OSError as erreur:
            print(f'Echec de connexion : {erreur}')
            time.sleep(2)





#on attend quelques ms pour s'assurer du chargement des librairies
time.sleep_ms(500)
print("================================")
print("|  Fil rouge : Etape 1 - IOT   |")
print("===============================")

#Loop
station=connexion_wifi()
client_mqtt = connexion_mqtt()

while True: 
    #récupère le temps de la boucle
    maintenant = time.ticks_ms() 
    if time.ticks_diff(maintenant, derniere_lecture)>= INTERVALLE_LECTURE_MS:
        derniere_lecture = maintenant
        #récup des infos de mon capteur
        try:
            capteur_temperature.measure()
            temperature = capteur_temperature.temperature()
            #Publish de la temperature sur mqtt
            payload=f'Il fait {temperature}°C dans le netlab'
            client_mqtt.publish(TOPIC_TEMPERATURE,payload)
            #Fin publication sur le topic temperature


            humidite = capteur_temperature.humidity()
            print(f'NETLAB 1 / Etage 1 : Temperature : {temperature:.1f} | Humidité : {humidite:.1f}')
        except OSError:
            print("Erreur de lecture du DHT22")
        
        #capteur de présence
        try:
            presence= pir.value()
            print(presence)
            presenceDetectee = 0
            if presence == 1 :
                presenceDetectee ="OUI"
            else:
                presenceDetectee ="NON"
            print(f'Présence : {presenceDetectee}')
        except OSError:
            print("Le PIR est arrivé")

        #capeur luminosité
        try:
            lum =ldr.read() #normalement entre 0 et 4095
            
            voltage = lum / 4095. * 5
            resistance = 2000 * voltage / (1 - voltage / 5)
            lux = math.pow(50 * 1e3 * math.pow(10, 0.7) / resistance, (1 / 0.7));
            Sombre = lux < SEUIL_LUMINOSITE

            print("Salle :", lux, ("sombre") if Sombre else ("Lumineux"))

        except OSError:
            print("Erreur capteur de luminosité")
    time.sleep_ms(10)    