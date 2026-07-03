# Algorithme triangle_pascal
# DEBUT
#     Variable nbreBase : Entier
#     CHECKERROR(nbreBase)

#     LOOP condition : nbreBase > 1(
#         ECRIRE(nbreBase)
#         SI nbreBase%2==0 ALORS
#             nbreBase //= 2
#         FINSI

#         SINON
#             nbreBase=nbreBase*3+1
        
    
#     )

# FIN

nbreDepart = int(input("Entrer un nombre: "))


while nbreDepart > 1 :
    print(nbreDepart)
    if nbreDepart%2==0 :
        nbreDepart //= 2
    else:
        nbreDepart = nbreDepart *3 +1
print("1")