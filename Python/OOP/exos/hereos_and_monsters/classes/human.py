from .hero import Hero

class Human(Hero):
    def __init__(self, name) -> None:
        super().__init__()
        self.force +=1
        self.endurance+=1
        self.max_vie = self.vie # Overwrite max vie
        self.name = name



