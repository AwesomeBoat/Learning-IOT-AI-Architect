"""
Loot system for Heroes vs Monsters game.

Defines Gold and Leather items that monsters drop.
"""

from v1.dice import roll_d6, roll_d4


class Loot:
    """Base class for all loot items."""
    
    def __init__(self) -> None:
        """Initialize a loot item."""
        pass
    
    def __repr__(self) -> str:
        """Return string representation of loot."""
        return f"{self.__class__.__name__}()"


class Gold(Loot):
    """Gold currency dropped by some monsters."""
    
    def __init__(self, amount: int) -> None:
        """
        Initialize a gold loot.
        
        Args:
            amount: Amount of gold
        """
        super().__init__()
        self.amount = amount
    
    @classmethod
    def generate(cls) -> "Gold":
        """
        Generate random gold amount (1d6).
        
        Returns:
            Gold instance with random amount
        """
        return cls(roll_d6())
    
    def __repr__(self) -> str:
        return f"Gold({self.amount})"


class Leather(Loot):
    """Leather material dropped by some monsters."""
    
    def __init__(self, amount: int) -> None:
        """
        Initialize leather loot.
        
        Args:
            amount: Amount of leather
        """
        super().__init__()
        self.amount = amount
    
    @classmethod
    def generate(cls) -> "Leather":
        """
        Generate random leather amount (1d4).
        
        Returns:
            Leather instance with random amount
        """
        return cls(roll_d4())
    
    def __repr__(self) -> str:
        return f"Leather({self.amount})"
