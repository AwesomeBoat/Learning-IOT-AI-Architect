# exo16-Un Higher or Lower game

from random import randint



def check_if_correct(target, guess):
    if guess < target :
        print(f"The number is higher than {guess}")
    elif guess > target :
        print(f"The number is lower than {guess}")
    elif guess == target :
        print(f"Congratulation, you won ! The number was {target}")


def main():
    is_running= True
    target=randint(0,101)
    print("Welcome to Guess The Number")
    guess=0

    # Game loop
    while guess != target:
        try:
            guess = int(input("Guess a number between 1 and 100 (-1 to exit): "))
            if guess == -1:
                is_running=False
                break
        except:
            print("Please enter only a number")
            continue
        check_if_correct(target, guess)
    restart = input("Would you like to restart ? y/N")

    # Exit
    if restart.upper() == "Y":
        main()
    else:
        print("Thanks for playing :)")
        is_running = False
        
    
main()

