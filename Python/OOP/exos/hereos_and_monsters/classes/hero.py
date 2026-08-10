from .caracter import Caracter


class Hero(Caracter):

    def __init__(self) -> None:
        super().__init__()
        self.bag = {
            "Leather" : 0,
            "Gold"  :0
        }
        self.max_vie = self.vie
        

    
    def rest(self):
        self.vie = self.max_vie