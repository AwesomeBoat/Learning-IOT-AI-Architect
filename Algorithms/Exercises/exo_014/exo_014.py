#  exo8-Lanceur de balles de tennis (Pseudo-Code + Python) 
# (Indice : 
# booleen = 
# bool(
# int(
# input(
# "Veuillez insérer : 1 = oui / 0 = non"
# Réaliser l’algorithme d’un lanceur de balles de tennis. Ce lanceur possède deux états :
# ))– prêt : permet de savoir si le tennisman est prêt. Il ne faut pas lancer de balles dans le cas contraire– panier_vide : permet de savoir s’il y a encore des balles disponibles
# Le lanceur de balle possède l’opération « lancerBalle » qui, vous l’aurez compris, permet de 
# lancer une balle.

# exo14-Reprenez l’algorithme du lanceur de balles de tennis et 
# faites en sorte qu’il lance une balle tant que le stock n’est pas 
# vide. Il y a donc 2 variables stock_balles et pret



def throw_tennis_ball(ball_basket, player_is_ready,):
    if ball_basket and player_is_ready:
        ball_basket -= 1
        print(f"The ball is throwed, {ball_basket} balls left")
        return ball_basket
    else:
        if ball_basket == 0:
            print("The basket is empty")
        else:
            print("The player is not ready")
        return ball_basket



def refill_basket(basket):
    amount = int(input("Enter the refill amount: "))
    basket += amount
    print(f"The basket now has {basket} balls")
    return basket 


def switch_player_state(player_state):
    if player_state:
        print("The player state is now : not_ready")
        return False
    else :
        print("The player state is now : ready")
        return True
    
    

def main():

    print("Welcome to the ball throwing machine ! ")

    is_running = True
    ball_basket = 0 
    player_is_ready = True

    while is_running:

        choice = int(input('Make a choice :\nFill the basket : 1 \nThrow the ball : 2 \nChange player state : 3 \nexit : 4. '))
        
        match choice:
            case 1:
                ball_basket = int(refill_basket(ball_basket))
            case 2:
                ball_basket = int(throw_tennis_ball(ball_basket, player_is_ready))
            case 3:
                player_is_ready = switch_player_state(player_is_ready)
            case 4:
                is_running = False
    



main()