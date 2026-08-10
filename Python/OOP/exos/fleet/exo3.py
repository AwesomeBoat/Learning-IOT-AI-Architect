# Héritage : Créer une classe Croiseur  et une classe Chasseur qui héritent de Vaisseau . Ajouter un attribut bouclier aux vaisseaux.
# Polymorphisme : Redéfinir attaquer() pour le Croiseur : il doit d'abord anéantir le bouclier de l'ennemi avant de toucher sa coque. Le Chasseur ne fait aucun dégât tant qu'il y a du bouclier.
# Composition : Créer une classe Escadre. Elle possède un nom et une liste de membres (objets Vaisseau).
# Méthode de groupe : Ajouter attaque_commune(cible) dans Escadre pour que tous les membres attaquent la cible simultanément.
# Action : Modifier le X-Wing et le TIE Fighter pour qu'ils soient des Chasseur. Créer un Croiseur Jedi qui sera un Croiseur. Créer un Croiseur Mon Calamari qui sera un Croiseur. Faire deux Escadre qui vont combattre l'une contre l'autre.



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





class Croiseur(Ship):

    def __init__(self, name, pv, power, shield):

        # Attribut de la classe parente Ship
        super().__init__(name, pv, power)

        # attribut de Croiseur
        self.shield = shield

    def shoot(self,target) :

        damage = random.randint( int(self.power/2), self.power)

        if target.shield > 0:
           
            print(f"{self.name} inflige {damage} dégâts au bouclier de {target.name}")
            target.shield -= damage
            return
        

        elif target.pv <= 0 :
            print(f"La cible {target.name} est déjà détruite ")

        else :
            print(f"{self.name} inflige {damage} dégâts à {target.name}")
            target.pv -= damage


        
        


class Chasseur(Ship):
    
    def __init__(self, name, pv, power, shield):

        # Attribut de la classe parente Ship
        super().__init__(name, pv, power)

        # attribut de Croiseur
        self.shield = shield

    def shoot(self,target) :

        if target.shield > 0:
            print(f"La cible est protégée par un bouclier, aucun dégat infligé.")
            return
        
        elif target.pv <= 0 :
            print(f"La cible {target.name} est déjà détruite ")

        else :
            damage = random.randint( int(self.power/2), self.power)
            print(f"{self.name} inflige {damage} dégâts à {target.name}")
            target.pv -= damage
    


class Escadre :

    def __init__(self,name,members_list):
        self.name = name
        self.members = members_list

    def coordinated_shoot(self,target):

        
        targeted_ship = random.choice(target.members)
        while targeted_ship.pv <= 0 :
            targeted_ship = random.choice(target.members)

        waiting = [] # Permet de retarder l'attaque du chasseur si la cible à un bouclier actif

        for ship in self.members :
            if targeted_ship.shield > 0 and isinstance(ship,Chasseur):
                waiting.append(ship)
                print(f"{self.name} is waiting for the shield to break.")
                continue
            else :
                ship.shoot(targeted_ship)

        for ship in waiting : # Chasseur attaque (même si le bouclier est encore présent)
            ship.shoot(targeted_ship)



# ------------------- Programme -------------------
# Création des vaisseaux
            
    # Chasseur
x_wing = Chasseur('X-Wing', 300, 35, 100)
tie_fighter = Chasseur('TIE Fighter', 200, 50, 80)
    # Croiseur
jedi = Croiseur("Jedi",200, 30, 50)
mon_calamari = Croiseur("Calamari",250,26,20)


# Creation des flottes
escadron_blanc = Escadre("Escadre des blancs",[x_wing,jedi])

escadron_rouge = Escadre("Escadre des rouges",[tie_fighter,mon_calamari])

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
print(f"\nUn combat commence entre {escadron_blanc.name} et {escadron_rouge.name} !")


while (x_wing.pv > 0 or jedi.pv > 0) and (tie_fighter.pv > 0 or mon_calamari.pv > 0) :
    print("\n")
    escadron_rouge.coordinated_shoot(escadron_blanc)
    escadron_blanc.coordinated_shoot(escadron_rouge)
    print('----')
    print(x_wing)
    print(tie_fighter)
    print(jedi)
    print(mon_calamari)

# Résultat du combat
print("\n")
if x_wing.pv <= 0 and jedi.pv <= 0 :
    print("L'escadron Rouge à gagné !")
elif tie_fighter.pv <= 0 and mon_calamari.pv  <= 0 :
    print("L'escadron Blanc à gagné !")
