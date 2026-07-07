# Algorithme Calculatrice
# DEBUT
#     Variable operand1, operand2 : Entier
#     Variable operator : Entier

#     DEMANDER(operand1)
#     DEMANDER(operateur)
#     DEMANDER(operand2)

#     SI opererand2=0 ALORS
#         ECRIRE("Erreur, la divison ne peux pas se faire avec 0")
#     FINSI

#     SI operateur="+" ALORS
#         ECRIRE(operand1 + operand2)
#     FINSI

#     SI operateur="-" ALORS
#         ECRIRE(operand1 - operand2)
#     FINSI

#     SI operateur="*" ALORS
#         ECRIRE(operand1 * operand2)
#     FINSI

#     SI operateur="+" ALORS
#         ECRIRE(operand1 / operand2)
#     FINSI
    
    
    
# FIN

operand1 = int(input("Entrer un nombre: "))
operator = input("Entrer un opérateur (+,-,*,/): ")
operand2 = int(input("Entrer un deuxième nombre: "))

if operand2 == 0 :
    print("Erreur, la divison ne peux pas se faire avec 0")

match operator:
    
    case "+":
        print("Le résultat est : ")
        print(operand1 + operand2)
    case "-":
        print("Le résultat est : ")
        print(operand1 - operand2)
    case "*":
        print("Le résultat est : ")
        print(operand1 * operand2)
    case "/":
        print("Le résultat est : ")
        print(operand1 / operand2)

