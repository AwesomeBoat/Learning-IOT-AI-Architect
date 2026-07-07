#  exo31-Réalisez un algorithme dans lequel nous devons rechercher une valeur 
# (entrée par l'utilisateur) dans un tableau d'entiers. 


# Create the list
def create_list():
    
    my_list = []

    for i in range(1000):
        my_list.append(i)

    return my_list



def find_index(target_list, target):
    if target in target_list:
        print(f"{target} is at index {target_list.index(target)}")

    else:
        print(f"{target} is not in the list")


   
def main():
    new_list = create_list()
    target = int(input("Enter a digit/number value: "))

    find_index(new_list, target)

main()

