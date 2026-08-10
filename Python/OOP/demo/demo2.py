class Animal:
    specie = 'Mammifère'

    def __init__(self, name, breed, nb_pows, surname):
        self._name = name
        self._surname = surname
        self.breed = breed
        self.is_hungry = True
        self.__nb_pows = nb_pows
        self.__nb_teeth = 42 #todo changer pour mettre les vraies valeurs quand on aura l'héritage
        
        
    # Le getter 
    # Permet de consulter la valeur (telle quelle ou modifiée)
    @property
    def name(self):
        return f'{self._name} aka {self._surname}'

    # Le getter 
    # Permet de consulter la valeur (telle quelle ou modifiée)
    @property
    def nb_teeth(self):
        return self.__nb_teeth

    # Le setter
    # Permet de faire des vérifications avant de modifier la valeur de l'attribut
    @nb_teeth.setter
    def nb_teeth(self, value):
        if(value > self.nb_teeth) : raise ValueError()
        if(value < 0) : raise ValueError()
        self.__nb_teeth = value

    # ---- Redéfinition Dunder Methods ----
    def __str__ (self):
     return f"--------------------------------------\n| Nom    : {self.name:<25} |\n| Race   : {self.breed:<25} |\n| Espèce : {Animal.specie:<25} |\n| Faim   : { 'oui' if self.is_hungry == True else 'non':<25} |\n--------------------------------------" 

    # pour rédéfinir ce qui est affiché quand on fait repr(object) (return "")
    def __repr__(self):
        return f'ceci est une représentation de {self._name}'

    # pour déclencher des fonctions lors de la suppression
    def __del__(self) :
        pass

    # ----- Surchage d'opérateur
    # Permet de modifier le comportement d'un opérateur
    # ici change le comportement Animal + Animal
    # Voir la liste de tous les opérateurs : https://docs.python.org/3/library/operator.html
    def __add__(self, other_animal):
        #todo vérifier que les deux animaux soient du même type et que l'un soit un mâle et l'autre une femelle
        print(f'Un nouvel animal est né de la reproduction entre {self._name} et {other_animal._name}')
        return Animal('Bébé', 'Chimère', 6, 'La créature')   


    # ------ Méthodes -------

    def makeNoise(self):
        print('Graouuuuu')

    def feed(self) :
        print(f'{self.name} vient de recevoir à manger')
        self.is_hungry = False

    def amputate(self): 
        if self.__nb_pows == 0:
            print(f'Malheureusement {self.name} n\'a déjà plus de pattes... 😢')
        else :
            self.__nb_pows -= 1
            print(f'{self.name} vient de se faire amputer d\'une patte 😱. Il lui en reste {self.__nb_pows}')


# Programme
chien_1 = Animal('Taylor', 'Corgi', 4, 'Le Tchoups')
chat_1 = Animal('Soup', 'Européen', 4, 'Le Soupeur')
chat_2 = Animal('Gudule', 'Siamois', 4, 'Dudule')



print(chien_1 is chat_1) # faux
print('\nVoici les données du chien :')
# print(f"Nom : {chien_1.name}   |   Race : {chien_1.breed}   |   Espèce : {Animal.specie}")
print(chien_1)

if chien_1.is_hungry == True :
    print(f'{chien_1.name} a faim')

chien_1.makeNoise()

print('\nVoici les données du chat :')
# print(f"Nom : {chat_1.name}   |   Race : {chat_1.breed}")
print(chat_1)

if chat_1.is_hungry == True :
    print(f'{chat_1.name} a faim')

chat_1.makeNoise()

chat_1.feed()
if chat_1.is_hungry == True :
    print(f'{chat_1.name} a faim')

print(chat_2)
# ---- Demo attribut "privé" ----
# chat_2.amputate()
# chat_2.amputate()
# chat_2.amputate()
# chat_2.amputate()
# chat_2.amputate()

# ---- Démo setter de dents qui fait une vérification ----
print(f'{chat_2.name} possède {chat_2.nb_teeth} dents')
chat_2.nb_teeth = 32
print(f'{chat_2.name} possède {chat_2.nb_teeth} dents')
# chat_2.nb_teeth = -6 # va provoquer une erreur
# print(f'{chat_2.name} possède {chat_2.nb_teeth} dents')

# ---- Dunder Methods ----
print("\n")
print(chat_2)
print(repr(chat_2))

# ---- Surchage de l'opérateur + ----
# print( chien_1 + chat_2 )
bebe = chien_1 + chat_2
print(bebe)




