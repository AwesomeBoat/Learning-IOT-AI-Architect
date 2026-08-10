from abc import ABC, abstractmethod

class Animal(ABC):

    def __init__(self, name : str, age : int, appetit :int):
        self.name = name
        self.age = age
        self.appetit = appetit

    # === Méthodes de classe ===


    def feed(self):
        self.appetit = 0

    # === Méthode abstraite ===
    @abstractmethod
    def species(self):
        pass


    # === Getter et Setter ===
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value

    @property
    def appetit(self):
        return self._appetit
    
    @appetit.setter
    def appetit(self, value):
        if  0 < value > 100:
            raise ValueError("L'appétit doit être compris entre 0 et 100")
        else:
            self._appetit = value

    # OU :
    
    # self._appetit = min(100, max(0,value))


