# Ecrire un algorithme qui demande à l’utilisateur de taper 10 entiers et qui affiche le plus petit de ces entiers.



def get_smaller_num(int_list):
    is_running = True
    smallest_num = int_list[0]

    while is_running:
        for element in int_list:
            if element < smallest_num:
                smallest_num = element

        exit_condition = int_list.index(element) == len(int_list) -1

        if exit_condition:
            is_running=False

    return smallest_num


def list_filler():

    int_list = []
    for n in range (10):
        num = int(input(f"Enter a number ({10-n} left): "))
        int_list.append(num)
    
    return int_list

def main():
    print("Welcome")
    user_list = list_filler()
    smaller_number = get_smaller_num(user_list)

    print(f"The smallest number of your list is {smaller_number}")


main()