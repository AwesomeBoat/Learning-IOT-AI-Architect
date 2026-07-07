# exo15-À l’aide de deux boucles, afficher les tables de 
# multiplication de 1 à 9. Ensuite, coder votre algorithme en 
# Python.

def display_times_table(i, j):
    while i < 9 and j < 9:
        for i in range(10):
            print(f"{i} * {j} = {i*j}")
            for j in range(10):
                print(f"{i} * {j} = {i*j}")




def optimized_times_table(n):
    for i in range (1,10):
        print(f"{i} * {n} = {i*n}")



display_times_table(1,1)

optimized_times_table(9)