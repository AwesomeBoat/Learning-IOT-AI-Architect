# exo22-BONUS : initialiser un tableau de 9 entiers 
# avec les valeurs 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 
# à l’aide d’une boucle. Ensuite, à l’aide d’une boucle 
# afficher la valeur de chaque cellule du tableau avec 
# l’opération Ecrire().

my_list = []
num = 1

# create list
for loop in range (10):
    my_list.append(2*num)
    num = 2*num

# print elements
for n in range(len(my_list)):
    print(my_list[n])


