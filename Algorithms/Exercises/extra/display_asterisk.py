#  2) Réalisez un algorithme qui demande un nombre à l'utilisateur et affiche autant de ligne que le nombre spécifié par 
# l'utilisateur.Exemple : l'utilisateur a rentré le nombre 5 et l'algorithme affiche :
# *
# **
# ***
# ****
# *****


def display_asterisk(amount):
    n = 1
    while n < amount + 1:
        print("*"*n)
        n+=1


def main():
    is_running = True

    while is_running:

        # Check if user input is valid
        try :
            number_of_line = int(input("Enter the amount of lines: "))
        except:
            print("Please enter only a number")


        display_asterisk(number_of_line)

        # Exit loop
        exit = input("Would you like to start again y/N : ")

        if exit.lower() == "y":
            is_running=False


main()