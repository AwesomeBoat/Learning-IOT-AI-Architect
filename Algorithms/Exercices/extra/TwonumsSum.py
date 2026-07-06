# TwoNumbersSum

# Exercice 1 – Addition de deux nombres
# Demander deux nombres à l'utilisateur et afficher leur somme.
# Exemple :
# Entrée :5 8 
# Sortie :La somme est 13. 



# list with both numbers



def two_number_sum(numbers):

    num_list = numbers.split()

    return(f"{num_list[0]} + {num_list[1]} = {int(num_list[0]) + int(num_list[1])}")


def check_numbers_input(numbers):
    
    splitted_nums=numbers.split()
    if len(splitted_nums) != 2:
        print("Error please enter only two digits")
        return False
    for num in splitted_nums:
        try:
            int(num)
        except ValueError:
            print("Error, please enter only digits or numbers")
            return False
    return True
    




def main():
    print("Hi, Welcome to the Two numbers sum program.")
    while True:

        numbers_input = input("Enter two number / digit, make sure to seperate them with a space: ")
        if check_numbers_input(numbers_input):
            print(two_number_sum(numbers_input))
            break




main()