"""
Hero classes for Heroes vs Monsters game.

Defines playable hero types: Human and Dwarf, with inventory system.
"""

from abc import abstractmethod
from v1.character import Character
from v1.dice import roll_best_three_d6
from v1.loot import Gold, Leather
from typing import Dict, Union


class Hero(Character):
    """
    Abstract base class for all hero types.
    
    Heroes can collect loot and restore HP after combat.
    """
    
    def __init__(
        self,
        name: str,
        strength: int,
        endurance: int,
        x: int = 0,
        y: int = 0,
    ) -> None:
        """
        Initialize a hero.
        
        Args:
            name: Hero name
            strength: Base strength
            endurance: Base endurance
            x: Starting x coordinate
            y: Starting y coordinate
        """
        super().__init__(name, strength, endurance, x, y)
        # Inventory: count of Gold and Leather items
        self.inventory: Dict[str, int] = {
            "gold": 0,
            "leather": 0,
        }
    
    def add_loot(self, loot: Union[Gold, Leather]) -> None:
        """
        Add loot to inventory.
        
        Args:
            loot: Gold or Leather item to add
        """
        if isinstance(loot, Gold):
            self.inventory["gold"] += loot.amount
        elif isinstance(loot, Leather):
            self.inventory["leather"] += loot.amount
    
    def get_inventory_string(self) -> str:
        """
        Get formatted inventory string.
        
        Returns:
            String showing current loot count
        """
        gold = self.inventory["gold"]
        leather = self.inventory["leather"]
        return f"Gold: {gold} | Leather: {leather}"
    
    def get_symbol(self) -> str:
        """Get hero's display symbol (H)."""
        return "H"
    
    @abstractmethod
    def __repr__(self) -> str:
        pass


class Human(Hero):
    """
    Human hero type.
    
    Bonuses: +1 Strength, +1 Endurance
    """
    
    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        """
        Initialize a human hero.
        
        Attributes are generated using 4d6 best-of-3, then +1 is added to both.
        
        Args:
            name: Hero name
            x: Starting x coordinate
            y: Starting y coordinate
        """
        base_strength = roll_best_three_d6()
        base_endurance = roll_best_three_d6()
        
        # Apply human bonuses
        strength = base_strength + 1
        endurance = base_endurance + 1
        
        super().__init__(name, strength, endurance, x, y)
    
    def __repr__(self) -> str:
        return (
            f"Human("
            f"name={self.name}, "
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )


class Dwarf(Hero):
    """
    Dwarf hero type.
    
    Bonuses: +2 Endurance (exceptional durability)
    """
    
    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        """
        Initialize a dwarf hero.
        
        Attributes are generated using 4d6 best-of-3, then +2 is added to endurance only.
        
        Args:
            name: Hero name
            x: Starting x coordinate
            y: Starting y coordinate
        """
        base_strength = roll_best_three_d6()
        base_endurance = roll_best_three_d6()
        
        # Apply dwarf bonuses
        strength = base_strength
        endurance = base_endurance + 2
        
        super().__init__(name, strength, endurance, x, y)
    
    def __repr__(self) -> str:
        return (
            f"Dwarf("
            f"name={self.name}, "
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )
