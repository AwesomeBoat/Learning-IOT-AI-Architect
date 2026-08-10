from classes.chippable_animal import Chippable_animal

class Dog(Chippable_animal):

    def __init__(self, name : str, age : int, appetit : int, race : str, chip_number = None):
        super().__init__(name, age, appetit, chip_number)
        self.race = race

    @property
    def species(self):
        return "Dog"
    
    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, value):
        self._race = value