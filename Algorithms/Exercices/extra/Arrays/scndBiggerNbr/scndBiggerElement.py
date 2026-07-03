# // Exercice : Trouver le deuxième plus grand élément

# // Objectif : Parcourir le tableau une seule fois.

# // Défi : Gérer les doublons et les tableaux très petits.



# Algorithme scndBigger
# DEBUT
#     Variable myArray : Entier
#     Variable Biggest : Entier
#     Variable scndBig : Entier

#     // Itérer tous les éléments de la liste
#     LOOP(range len(myArray))( // for in
    
#         SI actualElem > Biggest ALORS
#             biggest = actualElem
#             //Sortir de l'itération
#         FINSI

#         ET SI actualElem > scndBig ALORS
#             scndBig = actualElem
#         FINSI
        
#     )

#     ECRIRE("The second biggest number is : ")



# FIN


myArray = [2,3,1,1,1,4,2,5,6,2,3,1,4,5,6,4,5,2,1,3,2,5,6,4,7]

biggest_int = 0
scnd_Biggest_int = 0
double = []
for element in myArray:
    if element in double:
        continue
    elif element == biggest_int or element == scnd_Biggest_int:
        double.append(element)
        continue
    if element > biggest_int:
        print(f"First upgraded to {element}")
        scnd_Biggest_int = biggest_int
        biggest_int = element
    elif element > scnd_Biggest_int:
        print(f"Second upgraded to {element}")
        scnd_Biggest_int = element

print(scnd_Biggest_int)
print(double)