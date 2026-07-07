#  1) Réalisez un système de connexion à l'aide d'un mot de passe. L'algorithme demande à l'utilisateur de saisir son mot 
# de passe. Si ce dernier valide de bon mot de passe, on le salue. Par contre, si il fait une erreur trois fois de suite, un 
# message lui signalera que son compte est bloqué et il ne pourra pas réessayer une quatrième fois


def check_password(password_try, valid_password):
    if password_try == valid_password:
        return True
    else:
        return False


def main():
    attemps = 3
    valid_password = "abcdefgH"
    is_connected = False

    while not is_connected and attemps > 0:
        password=input("Enter your password: ")

        if  check_password(password, valid_password):
            print("Welcome :)")
            is_connected = True
            break
        
        else:
            print(f"Wrong password, {attemps -1} attemps left !")
            attemps -= 1

    if attemps <= 0 :
        print("Your account is blocked")


main()
    





