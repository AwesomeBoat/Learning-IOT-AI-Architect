import random
class Voiture:

    def __init__(self,name,min_speed,max_speed):
        self.__max_speed = max_speed
        self.__min_speed = min_speed
        self._name = name
        self.lap_counter = 0

    

class Course:
    
    def __init__(self, nbr_car):
        self.__nbr_car = []

