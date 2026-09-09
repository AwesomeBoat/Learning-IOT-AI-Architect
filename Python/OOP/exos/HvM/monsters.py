"""
Monster classes for Heroes vs Monsters game.

Defines enemy types: Wolf, Orc, and Dragonlet.
"""

from abc import abstractmethod
from v1.character import Character
from v1.dice import roll_best_three_d6
from v1.loot import Gold, Leather
from typing import List


class Monster(Character):
    """
    Abstract base class for all monster types.
    
    Monsters can be defeated and drop loot.
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
        Initialize a monster.
        
        Args:
            name: Monster name/type
            strength: Base strength
            endurance: Base endurance
            x: Starting x coordinate
            y: Starting y coordinate
        """
        super().__init__(name, strength, endurance, x, y)
    
    def generate_loot(self) -> List[object]:
        """
        Generate loot items this monster drops.
        
        Returns:
            List of Loot items (Gold and/or Leather)
        """
        return []
    
    @abstractmethod
    def get_symbol(self) -> str:
        """Get monster's display symbol."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass


class Wolf(Monster):
    """
    Wolf monster type.
    
    Drops: Leather
    """
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initialize a wolf.
        
        Stats are generated using 4d6 best-of-3 (no bonuses).
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        strength = roll_best_three_d6()
        endurance = roll_best_three_d6()
        
        super().__init__("Wolf", strength, endurance, x, y)
    
    def generate_loot(self) -> List[object]:
        """
        Generate wolf loot (leather only).
        
        Returns:
            List containing one Leather item
        """
        return [Leather.generate()]
    
    def get_symbol(self) -> str:
        """Get wolf's display symbol (L)."""
        return "L"
    
    def __repr__(self) -> str:
        return (
            f"Wolf("
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )


class Orc(Monster):
    """
    Orc monster type.
    
    Bonuses: +1 Strength
    Drops: Gold
    """
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initialize an orc.
        
        Stats are generated using 4d6 best-of-3, then +1 is added to strength.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        base_strength = roll_best_three_d6()
        endurance = roll_best_three_d6()
        
        # Apply orc bonus
        strength = base_strength + 1
        
        super().__init__("Orc", strength, endurance, x, y)
    
    def generate_loot(self) -> List[object]:
        """
        Generate orc loot (gold only).
        
        Returns:
            List containing one Gold item
        """
        return [Gold.generate()]
    
    def get_symbol(self) -> str:
        """Get orc's display symbol (O)."""
        return "O"
    
    def __repr__(self) -> str:
        return (
            f"Orc("
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )


class Dragonlet(Monster):
    """
    Dragonlet monster type.
    
    Bonuses: +1 Endurance
    Drops: Gold and Leather (as it can be both hunted for treasure and skinned)
    """
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initialize a dragonlet.
        
        Stats are generated using 4d6 best-of-3, then +1 is added to endurance.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        strength = roll_best_three_d6()
        base_endurance = roll_best_three_d6()
        
        # Apply dragonlet bonus
        endurance = base_endurance + 1
        
        super().__init__("Dragonlet", strength, endurance, x, y)
    
    def generate_loot(self) -> List[object]:
        """
        Generate dragonlet loot (both gold and leather).
        
        Returns:
            List containing one Gold and one Leather item
        """
        return [Gold.generate(), Leather.generate()]
    
    def get_symbol(self) -> str:
        """Get dragonlet's display symbol (D)."""
        return "D"
    
    def __repr__(self) -> str:
        return (
            f"Dragonlet("
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )
