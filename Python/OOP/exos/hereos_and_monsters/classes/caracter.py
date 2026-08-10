from random import randint

def roll_dices():
    ' generate the 3 biggest value of a 6 dices roll'
    dices = [randint(1,6),randint(1,6),randint(1,6),randint(1,6)]
    return sum(sorted(dices, reverse=True)[:3])



class Caracter:

    def __init__(self) -> None: 
        self.endurance = roll_dices()
        self.force = roll_dices()
        self.vie = (self.endurance*2.5)+self.endurance


    @property
    def vie(self):
        return self._vie

    @vie.setter
    def vie(self,value):
        self._vie = max(0,value)

    # Methods 
    def hit(self,target):
        damages = randint(1,4)
        if self.force < 5 :
            damages-=1
        elif self.force < 15 :
            damages += 1
        else:
            damages += 2
        
        target.vie -= damages
        return damages





        
