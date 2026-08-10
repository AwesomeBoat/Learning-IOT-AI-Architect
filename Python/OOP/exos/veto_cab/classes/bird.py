from classes.animal import Animal

class Bird(Animal):

    def __init__(self, name: str, age: int, appetit: int, color : str):
        super().__init__(name, age, appetit)
        self.color = color

    # Setter et getter
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value : str):
        self._color = value

    @property
    def species(self):
        return "Bird"