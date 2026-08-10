if __name__ == "__main__":
    from rabbit import Rabbit
    from dog import Dog
    from bird import Bird
    from chippable_animal import Chippable_animal
    from animal import Animal

else :
    from classes.rabbit import Rabbit
    from classes.dog import Dog
    from classes.bird import Bird
    from classes.chippable_animal import Chippable_animal
    from classes.animal import Animal

class Cabinet:

    def __init__(self):
        self.animals : list[Animal] = []


    @property
    def animals(self):
        return self._animals

    @animals.setter
    def animals(self, animals):
        self._animals = animals

    
    def add_animal(self, animal):
        if animal.__class__.__name__ in ["Dog", "Rabbit", "Bird"]:
            self.animals.append(animal)
        else :
            raise ValueError("The animal isn't correct")
        
    
    # === Methods ===
    
    def old_check_up(self):
        for animal in self.animals:
            print(f"Name : {animal.name}")
            print(f"Species : {animal.species}")
            print(f"Age : {animal.age}")
            print(f"Appetite : {animal.appetit}")
            if isinstance(animal, Chippable_animal):  
                print(f"Chip number : {animal.chip_number}")
            print(50*"-")

    def check_up(self):
        for animal in self.animals :
            print(f'nom: {animal.name} / espece: {animal.species} / appetit %:{animal.appetit} / numero_puce: {animal.chip_number if isinstance(animal, Chippable_animal) else 'No chip'}')
            print(50*"-")
    def feed_animals(self):
        for animal in self.animals :
            animal.feed()

    
# Check_up en Ternaire
"""
def check_up(self):
for elem in self._animaux:
    print(f'{elem.nom} / {elem.species} / {elem.appetit} {elem.chip_number if isinstance(elem, Chippable_animal) else ""}')

Permet de renvoyer une valeur ssi la condition est vraie, sinon ..
"""