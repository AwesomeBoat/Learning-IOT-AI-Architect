# Les fondamentaux :
# Créer une classe 

class Animal:
    # Attribut de classe
    specie = 'Mammifère'

    # la méthode __init__ sert à initialiser les données de l'objet instancié (constructeur)
    # self est un mot-clef qui fait référence à l'objet actuellement en train d'être instancié
    def __init__(self, name, breed, nb_pows, surname):
        self._name = name
        self._surname = surname
        self.breed = breed
        self.is_hungry = True
        self.__nb_pows = nb_pows
        self.__nb_teeth = 42
    # méthodes
    def makeNoise(self):
        print('Graouuuuu')

    def feed(self) :
        print(f'{self.name} vient de recevoir à manger')
        self.is_hungry = False

    def amputate(self):
        if self.__nb_pows == 0:
            print(f"Malheureusement {self.name} n'a déjà plus de pattes")   
        else:
            self.__nb_pows -= 1

    # getter
    @property
    def name(self):
        return f"{self._name} aka {self._surname}"
    
    @property
    def nb_teeth(self):
        return self._nb_teeth

    # setter 
    @nb_teeth.setter
    def nb_teeth(self, value):
        if (value < 0) : raise ValueError()
        self.__nb_teeth = value




# Créer une nouvelle instance à partir de la classe Animal
chien_1 = Animal('Taylor', 'Corgi', 4,'le Tchoups')
chat_1 = Animal('Soup', 'Européen', 4,"Le Soupeur")

print(chien_1 is chat_1) # faux
print('\nVoici les données du chien :')
print(f"Nom : {chien_1.name}   |   Race : {chien_1.breed}   |   Espèce : {Animal.specie}")

if chien_1.is_hungry == True :
    print(f'{chien_1.name} a faim')

chien_1.makeNoise()

print('\nVoici les données du chat :')
print(f"Nom : {chat_1.name}   |   Race : {chat_1.breed}")

if chat_1.is_hungry == True :
    print(f'{chat_1.name} a faim')

chat_1.makeNoise()

chat_1.feed()
if chat_1.is_hungry == True :
    print(f'{chat_1.name} a faim')



