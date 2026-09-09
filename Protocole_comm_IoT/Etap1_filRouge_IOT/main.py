import dht
import time
from machine import Pin

#Config des numéro de pin pour les branchements
BROCHE_DHT22 = 2
#création de l'objet contrôlant mon DHT22
capteur_temperature = dht.DHT22(Pin(BROCHE_DHT22))

#Variable
INTERVALLE_LECTURE_MS= 2000
derniere_lecture = 0

#on attend quelques ms pour s'assurer du chargement des librairies
time.sleep_ms(500)
print("================================")
print("|  Fil rouge : Etape 1 - IOT   |")
print("===============================")

#Loop
while True: 
    #récupère le temps de la boucle
    maintenant = time.ticks_ms() 
    if time.ticks_diff(maintenant, derniere_lecture)>= INTERVALLE_LECTURE_MS:
        derniere_lecture = maintenant
        #récup des infos de mon capteur
        try:
            capteur_temperature.measure()
            temperature = capteur_temperature.temperature()
            humidite = capteur_temperature.humidity()
            print(f'NETLAB 1 / Etage 1 : Temperature : {temperature:.1f} | Humidité : {humidite:.1f}')
        except OSError:
            print("Erreur de lecture du DHT22")
    time.sleep_ms(10)    