# Algorithme ConvertToSecond
# DEBUT
#     Variable sec: Entier
#     Variable hours : Entier
#     Variable min : Entier
#     Variable days : Entier
#     Variable sec2: Entier
#     Variable hours2 : Entier
#     Variable min2 : Entier
#     Variable days2 : Entier

#     Variable totalSec : Entier
#     Variable totalSec2 : Entier

#     totalSec = sec + hours*3600 + min *60 + days * 3600*24
#     totalSec2 = sec2 + hours2*3600 + min2 *60 + days2 * 3600*24
    
#     ECRIRE("La différence entre les deux est de : ")
# FIN

sec = int(input("Secondes 1: "))
min = int(input("Minutes 1: "))
hour = int(input("hours 1: "))
days = int(input("Days 1 :"))

sec2 = int(input("Secondes 2: "))
min2 = int(input("Minutes 2: "))
hour2 = int(input("hours 2: "))
days2 = int(input("Days 2 :"))

totalSec = sec + hour*3600 + min *60 + days * 3600*24
totalSec2 = sec2 + hour2*3600 + min2 *60 + days2 * 3600*24

print(f"La différence entre les deux est de : {totalSec - totalSec2} secondes")


