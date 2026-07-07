#  4) Algorithme demandant 3 nombres : nbRep, nbTiret, nbEspace. Ce dernier affiche à l'écran autant de tiret que la 
# valeur de nbTiret, suivi d'autant d'espace que la valeur de nbEspace. Le tout autant de fois que la valeur de 
# nbRep.Exemple : si nbRep = 2, nbTiret = 1 et nbEspace = 3 le résultat est le suivant :|-   -  |




def generate_display(rep, tiret, espace):
    output_display = "|"
    for rep in range (rep):
        for dash in range(tiret):
            output_display += "-"
        for space in range(espace):
            output_display += " "
    output_display += "|"

    return output_display

def main():
    nb_rep = int(input("Enter the number of repetition: "))
    nb_tiret = int(input("Enter the number of '-': "))
    nb_espace = int(input("Enter the number of spaces: "))

    display = generate_display(nb_rep, nb_tiret, nb_espace)

    print(display)

main()