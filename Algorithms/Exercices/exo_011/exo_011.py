# Algorithme Appreciation
# DEBUT
#     Variable note : Entier
#     Variable run : Bool
#     Variable running = False
#     DEMANDER(note)

#     SI 0 > note > 20 ALORS
#         ECRIRE("Erreur, note non valide")
#         RELANCER(Appreciation)
#     FINSI

#     SI note <= 5 ALORS
#         ECRIRE("Très Mauvais")
#     FINSI

#     SI note < 10 ALORS
#         ECRIRE("Mauvais")
#     FINSI

#     SI 10 < note < 15 ALORS
#         ECRIRE("Bon")
#     FINSI

#     SI 15 <= note ALORS
#         ECRIRE("Très Bon")
#     FINSI
    

    
    
# FIN

note = -1
while note < 0 or note > 20 :
    note = int(input("Entrer une note: "))
    if note <= 5:
        print("très mauvais")
    
    
    elif note < 10:
        print("Mauvais")
        break

    elif 10 < note < 15:
        print("Bon")
        break

    elif 15<= note and note <= 20 : 
        print("Très bon")
        break
    
    else :
        print("Note non valide")

#     SI 10 < note < 15 ALORS
#         ECRIRE("Bon")
#     FINSI

#     SI 15 <= note ALORS
#         ECRIRE("Très Bon")
#     FINSI