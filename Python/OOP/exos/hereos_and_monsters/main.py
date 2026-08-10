from classes.hero import Hero
from classes.human import Human
from classes.monster import Monster
from classes.caracter import Caracter
from classes.dwarf import Dwarf
from classes.orc import Orc
from classes.wolf import Wolf
from classes.dragon import Dragon
import time




# Create hereos 

human1 = Human("Eric")
dwarf1 = Dwarf("Ferrero")

wolf1 = Wolf()
orc1 = Orc()
dragon1=Dragon()

def main():
    
    fight(human1,wolf1)
        
        


def fight(hero, monster):
    monster_name = monster.__class__.__name__
    while hero.vie > 0 and monster.vie > 0 :
        damage = hero.hit(monster)
        print(f"{hero.name} hit {monster_name} and dealt {damage} dmg, {monster_name} life is {monster.vie} ")
        time.sleep(0.5)
        damage = monster.hit(hero)
        print(f"{monster_name} hit {hero.name} and dealt {damage} dmg, {hero.name} life is {hero.vie}")
        time.sleep(0.5)
    

main()