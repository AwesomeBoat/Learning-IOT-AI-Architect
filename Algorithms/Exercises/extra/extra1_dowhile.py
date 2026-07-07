selection = -1
isTrue = True

while isTrue:
    selection = int(input("Entrez un nombre entre 1 et 10: "))
    if selection < 1 or selection >10:
        selection = int(input("Valeur incorrecte réessayer: "))
    else:
        isTrue = False




