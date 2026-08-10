from classes.animal import Animal

class Chippable_animal(Animal):

    def __init__(self, name : str, age : int, appetit:  int, chip_number = None):
        super().__init__(name, age, appetit)
        self.chip_number = chip_number

    
    @property
    def chip_number(self):
        if self._chip_number == None:
            return "Not-chipped"
        
        else :
            return self._chip_number
    
    @chip_number.setter
    def chip_number(self, value):
        self._chip_number = value