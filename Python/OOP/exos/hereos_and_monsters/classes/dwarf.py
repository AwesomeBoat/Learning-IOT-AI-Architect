from .hero import Hero

class Dwarf(Hero):
    def __init__(self,name) -> None:
        super().__init__()
        self.endurance +=2
        self.vie += 5
        self.max_vie = self.vie # Overwrite max vie
        self.name = name



