# Algorithme triangle_pascal
# DEBUT
#     Variable nbreBase : Entier
#     Variable n : Entier
#     Variable nbreLayer : Entier
#     Variable nbreEspace : Entier
#     n = 0
#     nbreLayer= (nbreBase//2)+1
#     nbreEspace = nbreLayer - 1


#     CHECKERROR(nbreBase)
#     Calculer(NbreLayer)
#     LOOP condition : n < nbreBase(
#         ECRIRE(nbreEspace*" ",n)
#         INCREMENTER(n)
#          DECREMENTER(nbreEspace)
#     )

# FIN


nbreBase=int(input("Entrer le nombre d'* de la base: "))
n = 1
nbreLayer = (nbreBase//2)+1
nbreEspace = nbreLayer - 1
nbreBaseinvert=nbreBase
while n<nbreBase:
    print(nbreEspace*" " , n*"*")
    n+=2
    nbreEspace-=1




#       *
#      ***
#     *****
#    *******
#   *********
#  ***********
# *************