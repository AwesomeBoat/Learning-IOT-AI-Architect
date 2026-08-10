from classes.chippable_animal import Chippable_animal


class Rabbit(Chippable_animal):

    def __init__(self, name : str, age : int, appetit : int, sex : str, chip_number = None):
        super().__init__(name, age, appetit, chip_number)
        self.sex = sex
        

    @property
    def species(self):
        return "Rabbit"
    
    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value