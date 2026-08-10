class Animal:

    def __init__(self, name, breed, nb_pows, surname):
        self._name = name
        self._surname = surname
        self.breed = breed
        self.is_hungry = True
        self.__nb_pows = nb_pows
        self._nb_teeth = 42

    @property
    def name(self):
        return f'{self._name} aka {self._surname}'

    @property
    def nb_teeth(self):
        return self._nb_teeth

   
    @nb_teeth.setter
    def nb_teeth(self, value):
        if(value > self.nb_teeth) : raise ValueError()
        if(value < 0) : raise ValueError()
        self._nb_teeth = value

    def __str__ (self):
     return f"--------------------------------------\n| Nom    : {self.name:<25} |\n| Race   : {self.breed:<25} |\n| Faim   : { 'oui' if self.is_hungry == True else 'non':<25} |\n--------------------------------------" 

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


class Mammal :
    def __init__(self, preg_dur):
        self.pregnancy_duration = preg_dur

    def give_birth(self):
        print(f"Un bébé est né après {self.pregnancy_duration} mois")

class Reptile :
    def __init__(self, hatch_time ):
        self.hatching_time = hatch_time

    def give_birth(self):
        print(f"Un oeuf a été pondu ! Il va éclore dans environ {self.hatching_time} jours")
 
class Dog(Animal, Mammal) :

    def __init__(self, name, breed, pows, surname, fav_toy) :
        # Appel de l'initialiseur des parents
        Animal.__init__(self, name, breed, pows, surname)
        Mammal.__init__(self, 2)
        # ajout de ce qui est propre au chien
        self.fav_toy = fav_toy
        # Redéfinition d'attribut 
        # Cet attribut existe dans animal mais on redéfinit sa valeur dans l'enfant
        self._nb_teeth = 42



    def snifSomeAss(self, target):
        print(f"{self._name} renifle les fesses de {target.name} pour dire bonjour")

    # Redéfinition de méthode
    # Cette méthode existe dans Animal et on redéfinit son comportement dans la classe enfant
    def makeNoise(self):
        print('Waf waf')

class Cat(Animal, Mammal):
    def __init__(self, name, breed, pows, surname, fav_hide) :
        Animal.__init__(self, name, breed, pows, surname)
        Mammal.__init__(self, 2)
        self.fav_hide = fav_hide
        self._nb_teeth = 30

    def destroyEverything(self): 
        print(f"{self.name} est en train de détruire tout dans la maison")

    def makeNoise(self):
        print('Miaouuuuu')

class Snake(Animal, Reptile):
    def __init__(self, name, breed, nb_pows, surname):
        Animal.__init__(self,name, breed, nb_pows, surname)
        Reptile.__init__(self, 80)
        self._nb_teeth = 50

    def makeNoise(self):
        print("Sssssssss")

class Rabbit(Animal) :
    def __init__(self, name, breed, nb_pows, surname):
        super().__init__(name, breed, nb_pows, surname)
        self._nb_teeth = 28

    def makeNoise(self):
        print('Skouick skouick')


class Person :
    def __init__(self, firstname, lastname) :
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self) :
        return f'{self.firstname} {self.lastname}'

class PetShop :
    def __init__(self, firstnameOwner, lasnameOwner) :
        self.pets = []
        self.owner = Person(firstnameOwner, lasnameOwner)

    def addPet(self, pet):
        self.pets.append(pet)


# Programme
animalerie = PetShop('JeanMi', 'Molette')
print(f'Gérant de l\'animalerie : {animalerie.owner}')


chien_1 = Dog('Taylor', 'Corgi', 4, 'Le Tchoups', 'Un os qui fait pouic')
chat_1 = Cat('Soup', 'Européen', 4, 'Le Soupeur', 'Son arbre')
chat_2 = Cat('Gudule', 'Siamois', 4, 'Dudule', 'Sous le canapé')
serpent_1 = Snake('Kaa', 'Grand Python', 0, 'L\'hypnotiseur')
lapin_1 = Rabbit('Panpan', 'Garenne', 4, 'Le tapeur fou')

animalerie.addPet(chien_1)


print(chien_1)
chien_1.makeNoise()
chien_1.snifSomeAss(chat_1)
print(chien_1.fav_toy)
print(chien_1.nb_teeth)
chien_1.give_birth()


print(chat_1)
chat_1.makeNoise()
chat_1.destroyEverything()
print(chat_1.fav_hide)
print(chat_1.nb_teeth)


print(serpent_1)
serpent_1.makeNoise()
serpent_1.give_birth()

print(lapin_1)
lapin_1.makeNoise()




