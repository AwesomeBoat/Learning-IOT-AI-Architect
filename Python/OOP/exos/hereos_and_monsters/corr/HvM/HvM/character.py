"""
Base character classes for Heroes vs Monsters game.

Defines the Character class and core mechanics for all game characters.
"""

from abc import ABC, abstractmethod
from v1.dice import roll_best_three_d6, roll_d4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Character(ABC):
    """
    Abstract base class for all game characters (Heroes and Monsters).
    
    Attributes:
        strength: Character's strength stat (3-18)
        endurance: Character's endurance stat (3-18)
        hp: Current hit points
        max_hp: Maximum hit points
        x: X coordinate on game board
        y: Y coordinate on game board
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
        Initialize a character.
        
        Args:
            name: Character name
            strength: Base strength value (before modifiers)
            endurance: Base endurance value (before modifiers)
            x: Starting x coordinate
            y: Starting y coordinate
        """
        self.name = name
        self.strength = strength
        self.endurance = endurance
        self.x = x
        self.y = y
        
        # Hit points = endurance + endurance modifier
        endurance_mod = self.calculate_modifier(self.endurance)
        self.max_hp = self.endurance + endurance_mod
        self.hp = self.max_hp
    
    @staticmethod
    def calculate_modifier(characteristic: int) -> int:
        """
        Calculate modifier based on characteristic value.
        
        Modifier scale:
        - < 5: -1
        - 5-9: 0
        - 10-14: +1
        - >= 15: +2
        
        Args:
            characteristic: The stat value to calculate modifier for
            
        Returns:
            Modifier value (-1, 0, +1, or +2)
        """
        if characteristic < 5:
            return -1
        elif characteristic < 10:
            return 0
        elif characteristic < 15:
            return 1
        else:
            return 2
    
    def strike(self, target: "Character") -> int:
        """
        Attack another character.
        
        Damage calculation: 1d4 + strength modifier (minimum 1)
        
        Args:
            target: The character being attacked
            
        Returns:
            Damage dealt
        """
        strength_mod = self.calculate_modifier(self.strength)
        base_damage = roll_d4()
        damage = max(1, base_damage + strength_mod)  # Minimum 1 damage
        
        target.take_damage(damage)
        return damage
    
    def take_damage(self, damage: int) -> None:
        """
        Reduce hit points by damage amount.
        
        Args:
            damage: Damage to take (should be positive)
        """
        self.hp = max(0, self.hp - damage)
    
    def is_alive(self) -> bool:
        """Check if character is still alive."""
        return self.hp > 0
    
    def heal_to_full(self) -> None:
        """Restore hit points to maximum (used after combat for heroes)."""
        self.hp = self.max_hp
    
    def get_symbol(self) -> str:
        """
        Get the character's display symbol on the game board.
        
        Returns:
            Single character symbol representing this character
        """
        return "?"
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"str={self.strength}, "
            f"end={self.endurance}, "
            f"hp={self.hp}/{self.max_hp}, "
            f"pos=({self.x},{self.y})"
            f")"
        )
    
    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"
