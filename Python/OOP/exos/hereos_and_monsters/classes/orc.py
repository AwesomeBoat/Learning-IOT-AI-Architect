from .monster import Monster
from random import randint

class Orc(Monster):

    def __init__(self) -> None:
        super().__init__()
        self.force += 1
        self.loot_gold = randint(1,6)