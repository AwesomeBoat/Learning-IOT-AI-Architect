#  exo21-Écrire un algorithme qui saisit 6 entiers et les 
# stocke dans un tableau, puis affiche le contenu de 
# ce tableau une fois qu’il est rempli

tab = []
for loop in range (6):
    tab.append(int(input("Enter a number: ")))


for n in range (6):
    print(tab[n])
