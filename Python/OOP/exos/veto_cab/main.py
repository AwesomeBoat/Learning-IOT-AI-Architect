
"""
Exercice 4 : Cabinet Vétérinaire

Thèmes : Orienté Objet, Abstraction, Polymorphisme, Encapsulation.
Contexte

Vous devez modéliser le système de gestion d'un cabinet vétérinaire accueillant différents types d'animaux.
1. Structure des Animaux

Tous les animaux partagent des caractéristiques communes, mais chacun possède des spécificités propres :

    Animal (Classe abstraite)

        Attributs :

            nom (Chaîne de caractères)

            age (Entier)

            appetit (Entier, représenté sous forme de pourcentage de 0 à 100).

        Règles métier :

            L'appétit ne doit jamais descendre en dessous de 0, ni dépasser 100.

            Chaque animal peut être nourri : cette action réinitialise son appétit à 0%.

            Définir une méthode abstraite pour récupérer l'espèce de l'animal.

    Lapin

        Spécificité : possède un sexe.

        Identification : peut posséder un numeroPuce (optionnel / nullable).

    Chien

        Spécificité : possède une race.

        Identification : peut posséder un numeroPuce (optionnel / nullable).

    Oiseau

        Spécificité : possède une couleur.

        Identification : ne possède pas de puce.

2. Le Cabinet Vétérinaire

La classe CabinetVeterinaire gère la liste de tous les animaux présents. Elle doit proposer les fonctionnalités suivantes :

    Ajout d'animaux : Pouvoir ajouter n'importe quel type d'animal à la liste.

    checkUp() : Parcourt tous les animaux du cabinet et affiche leurs informations essentielles :

        Le nom

        L'espèce

        Le niveau d'appétit actuel

        Le numéro de puce (uniquement s'il existe).

    entretenir() : Exécute la maintenance du cabinet en nourrissant l'ensemble des animaux enregistrés.


"""


from classes.cabinet import *

# Create the cabinet
mon_cabinet = Cabinet()

# Add Animals to the cabinet
mon_cabinet.add_animal(Dog("Luffy",5,50,"Berger Allemand"))
mon_cabinet.add_animal(Rabbit("Goomba",5,50,"Male","065409840984"))
mon_cabinet.add_animal(Bird("Goomba",5,50,"Blue"))

# Check up the cabinet
mon_cabinet.check_up()

# Feed the animals
mon_cabinet.feed_animals()

# check again
mon_cabinet.check_up()


