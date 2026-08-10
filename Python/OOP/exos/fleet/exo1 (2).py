# Exercice 1 - Mise à feu (Syntaxe & Instances) Page
# Objectif : Créer ton premier chasseur.
# Classe : Crée une classe Vaisseau.
# Attributs : nom, pv (points de vie), puissance_feu.
# Attribut de classe : flotte (une liste vide qui stocke chaque instance de vaisseau créée).
# Méthode : attaquer(cible) qui soustrait la puissance_feu des pv de la cible.
# Action : Instancie un "X-Wing" et un "TIE Fighter". Lance un duel dans une boucle while jusqu'à ce que l'un des deux atteigne 0 PV.

import random


class Ship :

    fleet = []

    def __init__(self, name, pv, power):
        self.name = name
        self.pv = pv
        self.power = power
        Ship.fleet.append(self) #ajout auto dans la flotte

    def shoot(self, target):
        if target.pv <= 0 :
            print(f"La cible {target.name} est déjà détruite ")

        damage = random.randint( int(self.power/2), self.power)
        print(f"{self.name} inflige {damage} dégâts à {target.name}")
        target.pv -= damage


# Programme
x_wing = Ship('X-Wing', 300, 35)
# Ship.fleet.append(x_wing)
tie_fighter = Ship('TIE Fighter', 200, 45)
# Ship.fleet.append(tie_fighter)

for ship in Ship.fleet :
    print(f"\nNom : {ship.name} \nPV : {ship.pv} ")


print(f"\nUn combat commence entre {x_wing.name} et {tie_fighter.name} !\n")
while x_wing.pv > 0 and tie_fighter.pv > 0 :
    print("\n")
    x_wing.shoot(tie_fighter)
    tie_fighter.shoot(x_wing)

print("\n")
if x_wing.pv <= 0 and tie_fighter.pv <= 0 :
    print('Les deux vaisseaux se sont entre-détruits')
elif x_wing.pv <= 0 :
    print('Le X-Wing est détruit !')
else :
    print('Le TIE Fighter est détruit !')