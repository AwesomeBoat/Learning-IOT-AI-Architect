# Exercice 2 - Blindage & Énergie (Encapsulation & Magie) Page
# Objectif : Protéger les systèmes critiques.
# Encapsulation : Rends les __pv et la__puissance_de_feu privés. Personne ne doit pouvoir tricher !
# Property : Utilise @property pour lire les PV et la puissance, et un setter pour les empêcher de descendre en dessous de 0.
# Dunder Magic :
#     Implémente __str__ pour afficher l'état : "[Nom] Coque: 80% | Armes: 20". 
#     (où coque est le % de pv par rapport au max de pv et où armes est la puissance de feu)
#     Implémente __gt__ (Greater Than) pour comparer deux vaisseaux : vaisseau1 > vaisseau2 doit comparer leur puissance.

import random

class Ship :

    fleet = []

    @property
    def pv(self) : # getter
        return self.__pv 

    @pv.setter #setter 
    def pv(self, value):
        # Si on essaie de mettre une valeur > que les pv max, on va mettre le max de pv
        if value > self.__max_pv :
            self.__pv = self.__max_pv
        elif value < 0 :
            self.__pv = 0 #si nouvelle valeur négatif, on cap à 0
        else :
            self.__pv = value

    @property
    def power(self) :
        return self.__power

    @power.setter
    def power(self, value):
        if value < 0 : raise ValueError('La puissance de feu ne peut être négative')
        self.__power = value

    def __init__(self, name, pv, power):
        self.name = name
        self.__pv = pv
        self.__max_pv = pv
        self.__power = power
        Ship.fleet.append(self)

    # Dunder
    def __str__ (self) :
        return f'[{self.name}] Coque: { int(self.pv / self.__max_pv * 100) }% | Armes: {self.power}'

    # Surcharge Op
    def __gt__(self, other) :
        return self.power > other.power
        if(self.power > other.power) :
            return True
        else :
            return False

    def shoot(self, target):
        if target.pv <= 0 :
            print(f"La cible {target.name} est déjà détruite ")

        damage = random.randint( int(self.power/2), self.power)
        print(f"{self.name} inflige {damage} dégâts à {target.name}")
        target.pv -= damage


# ------------------- Programme -------------------
# Création des vaisseaux
x_wing = Ship('X-Wing', 300, 35)
tie_fighter = Ship('TIE Fighter', 200, 50)

# Affichage de la flotte
print("\n")
for ship in Ship.fleet :
    print(ship)

# Test setters
# x_wing.pv -= 310
# print(f"\nNom : {x_wing.name} \nPV : {x_wing.pv} ")   
# x_wing.pv += 500
# print(f"\nNom : {x_wing.name} \nPV : {x_wing.pv} ")
# x_wing.power = -5 #renvoie une erreur

# Combat
print(f"\nUn combat commence entre {x_wing.name} et {tie_fighter.name} !")
if x_wing > tie_fighter :
    print('Le X-Wing est plus puissant')
elif tie_fighter > x_wing :
    print('Le TIE Fighter est plus puissant')
else :
    print('Les 2 vaisseaux ont une puissance égale')


while x_wing.pv > 0 and tie_fighter.pv > 0 :
    print("\n")
    x_wing.shoot(tie_fighter)
    tie_fighter.shoot(x_wing)
    print('----')
    print(x_wing)
    print(tie_fighter)

# Résultat du combat
print("\n")
if x_wing.pv <= 0 and tie_fighter.pv <= 0 :
    print('Les deux vaisseaux se sont entre-détruits')
elif x_wing.pv <= 0 :
    print('Le X-Wing est détruit !')
else :
    print('Le TIE Fighter est détruit !')