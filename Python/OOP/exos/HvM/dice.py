"""
Dice rolling utilities for Heroes vs Monsters game.

Provides functions for rolling dice and generating character attributes.
"""

import random
from typing import List


def roll_dice(num_dice: int, num_faces: int) -> List[int]:
    """
    Roll multiple dice and return individual results.
    
    Args:
        num_dice: Number of dice to roll
        num_faces: Number of faces per die
        
    Returns:
        List of individual dice results
    """
    return [random.randint(1, num_faces) for _ in range(num_dice)]


def roll_best_three_d6() -> int:
    """
    Roll 4d6 and keep the best 3 (standard RPG attribute generation).
    
    Returns:
        Sum of the 3 best rolls out of 4d6
    """
    rolls = roll_dice(4, 6)
    rolls.sort()
    # Remove the lowest roll, keep the 3 best
    return sum(rolls[1:])


def roll_d4() -> int:
    """Roll a single 4-sided die."""
    return random.randint(1, 4)


def roll_d6() -> int:
    """Roll a single 6-sided die."""
    return random.randint(1, 6)
