from .monster import Monster
from random import randint

class Dragon(Monster):

    def __init__(self) -> None:
        super().__init__()
        self.loot_leather = randint(1,4)
        self.loot_gold = randint(1,6)