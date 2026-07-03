# Algorithme Distributeur
# DEBUT
#     Variable stock : Bool
#     Variable coca, sprite, fanta, eau, jus d'orange : string

#     ECRIRE("Entrer votre choix: ")
#     SI stock = False ALORS
#         print("Désole, il n'y a plus de stock")
#     FINSI
    
#     SI choix = 1 ALORS
#         print("Votre coca arrive")
#     FINSI

#     SI choix = 2 ALORS
#         print("Votre sprite arrive")
#     FINSI

#     SI choix = 3 ALORS
#         print("Votre fanta arrive")
#     FINSI

#     SI choix = 4 ALORS
#         print("Votre eau arrive")
#     FINSI

#     SI choix = 5 ALORS
#         print("Votre jus d'orange arrive")
#     FINSI
    
# FIN

stock = 10

choix=int(input("Sélectionner une boisson : coca: 1, sprite: 2, fanta: 3, eau: 4, jus d'orange: 5"))

if not stock :
    print("Désole, il n'y a plus de stock")

match choix:
    case 1:
        print("Votre coca arrive")
    case 2:
        print("Votre sprite arrive")
    case 3:
        print("Votre fanta arrive")
    case 4:
        print("Votre eau arrive")
    case 5:
        print("Votre jus d'orange arrive")