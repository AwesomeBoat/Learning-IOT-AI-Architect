"""
Game engine for Heroes vs Monsters game.

Contains combat system, game board, and main game loop.
"""

import random
from typing import List, Optional, Tuple
from v1.character import Character
from v1.heroes import Hero
from v1.monsters import Monster


class Combat:
    """
    Manages combat between two characters.
    
    Handles turn-based combat, damage resolution, and loot transfer.
    """
    
    def __init__(self, attacker: Character, defender: Character) -> None:
        """
        Initialize a combat between two characters.
        
        Args:
            attacker: The attacking character
            defender: The defending character
        """
        self.attacker = attacker
        self.defender = defender
        self.rounds = 0
        self.combat_log: List[str] = []
    
    def resolve_round(self) -> bool:
        """
        Resolve a single round of combat.
        
        The attacker strikes the defender. If defender dies, returns True.
        
        Returns:
            True if defender is dead, False if still alive
        """
        self.rounds += 1
        
        # Attacker strikes defender
        damage = self.attacker.strike(self.defender)
        log_entry = (
            f"Round {self.rounds}: {self.attacker.name} strikes {self.defender.name} "
            f"for {damage} damage! {self.defender.name} HP: {self.defender.hp}/{self.defender.max_hp}"
        )
        self.combat_log.append(log_entry)
        
        # Check if defender is dead
        if not self.defender.is_alive():
            self.combat_log.append(f"{self.defender.name} is defeated!")
            return True
        
        # Defender counterattacks (if both are still alive)
        damage = self.defender.strike(self.attacker)
        log_entry = (
            f"Round {self.rounds}: {self.defender.name} counterattacks {self.attacker.name} "
            f"for {damage} damage! {self.attacker.name} HP: {self.attacker.hp}/{self.attacker.max_hp}"
        )
        self.combat_log.append(log_entry)
        
        # Check if attacker is dead
        if not self.attacker.is_alive():
            self.combat_log.append(f"{self.attacker.name} is defeated!")
            return True
        
        return False
    
    def fight_to_death(self) -> Character:
        """
        Run combat until one character dies.
        
        Returns:
            The winning character
        """
        while self.attacker.is_alive() and self.defender.is_alive():
            if self.resolve_round():
                break
        
        return self.attacker if self.attacker.is_alive() else self.defender
    
    def get_log(self) -> str:
        """
        Get the full combat log as a formatted string.
        
        Returns:
            Multi-line combat log
        """
        return "\n".join(self.combat_log)
    
    def __repr__(self) -> str:
        return (
            f"Combat({self.attacker.name} vs {self.defender.name}, "
            f"rounds={self.rounds})"
        )


class Board:
    """
    Game board for Heroes vs Monsters.
    
    15x15 grid with 10 randomly placed monsters and one hero.
    Monsters are hidden until discovered by combat.
    """
    
    WIDTH = 15
    HEIGHT = 15
    NUM_MONSTERS = 10
    MIN_MONSTER_SPACING = 2
    
    def __init__(self) -> None:
        """Initialize the game board."""
        self.hero: Optional[Hero] = None
        self.monsters: List[Monster] = []
        self.discovered_monsters: List[Monster] = []  # Monsters visible on map
    
    def place_hero(self, hero: Hero, x: int = 0, y: int = 0) -> None:
        """
        Place hero on the board at given coordinates.
        
        Args:
            hero: The hero to place
            x: X coordinate (0-14)
            y: Y coordinate (0-14)
            
        Raises:
            ValueError: If coordinates are out of bounds
        """
        if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
            raise ValueError(f"Invalid hero position ({x}, {y})")
        
        hero.x = x
        hero.y = y
        self.hero = hero
    
    def place_monsters(self, monsters: List[Monster]) -> None:
        """
        Place all monsters on the board.
        
        Monsters are spaced at least MIN_MONSTER_SPACING (2) cells apart
        horizontally and vertically.
        
        Args:
            monsters: List of Monster objects to place
        """
        self.monsters = monsters
        for monster in self.monsters:
            self._find_valid_position(monster)
    
    def _find_valid_position(self, monster: Monster) -> None:
        """
        Find a valid position for a monster on the board.
        
        Valid position: at least MIN_MONSTER_SPACING cells away from all other
        monsters and from the hero.
        
        Args:
            monster: Monster to place
        """
        max_attempts = 100
        attempt = 0
        
        while attempt < max_attempts:
            x = random.randint(0, self.WIDTH - 1)
            y = random.randint(0, self.HEIGHT - 1)
            
            # Check spacing from other monsters
            valid = True
            for other in self.monsters:
                if other == monster:
                    continue
                if self._distance(x, y, other.x, other.y) < self.MIN_MONSTER_SPACING:
                    valid = False
                    break
            
            # Check spacing from hero
            if valid and self.hero:
                if self._distance(x, y, self.hero.x, self.hero.y) < self.MIN_MONSTER_SPACING:
                    valid = False
            
            if valid:
                monster.x = x
                monster.y = y
                return
            
            attempt += 1
        
        # Fallback: place anywhere if too many attempts
        monster.x = random.randint(0, self.WIDTH - 1)
        monster.y = random.randint(0, self.HEIGHT - 1)
    
    def _distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        Calculate Chebyshev distance (max of dx, dy) between two points.
        
        This is the grid distance used for spacing validation.
        
        Args:
            x1, y1: First point coordinates
            x2, y2: Second point coordinates
            
        Returns:
            Chebyshev distance
        """
        return max(abs(x1 - x2), abs(y1 - y2))
    
    def is_adjacent(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """
        Check if two positions are adjacent (horizontally or vertically).
        
        Adjacent means exactly 1 square away horizontally or vertically.
        Diagonal does NOT count as adjacent for combat triggering.
        
        Args:
            x1, y1: First position
            x2, y2: Second position
            
        Returns:
            True if horizontally or vertically adjacent
        """
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        
        # Adjacent: one is 0, other is 1 (and not both 1 = not diagonal)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
    
    def can_move(self, x: int, y: int) -> bool:
        """
        Check if a position is valid (within board bounds).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is valid
        """
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT
    
    def move_hero(self, new_x: int, new_y: int) -> Optional[Monster]:
        """
        Move hero to a new position.
        
        If hero moves adjacent to a monster, that monster is discovered.
        
        Args:
            new_x: Target X coordinate
            new_y: Target Y coordinate
            
        Returns:
            Monster if hero is now adjacent to one, None otherwise
            
        Raises:
            ValueError: If new position is invalid
        """
        if not self.can_move(new_x, new_y):
            raise ValueError(f"Cannot move to ({new_x}, {new_y})")
        
        if not self.hero:
            raise RuntimeError("No hero on board")
        
        self.hero.x = new_x
        self.hero.y = new_y
        
        # Check for adjacent monsters
        for monster in self.monsters:
            if monster.is_alive() and self.is_adjacent(
                self.hero.x, self.hero.y,
                monster.x, monster.y
            ):
                # Discover the monster
                if monster not in self.discovered_monsters:
                    self.discovered_monsters.append(monster)
                return monster
        
        return None
    
    def get_adjacent_monster(self) -> Optional[Monster]:
        """
        Get any live monster adjacent to the hero.
        
        Used to check if hero is in combat range.
        
        Returns:
            An adjacent live monster, or None
        """
        if not self.hero:
            return None
        
        for monster in self.monsters:
            if monster.is_alive() and self.is_adjacent(
                self.hero.x, self.hero.y,
                monster.x, monster.y
            ):
                if monster not in self.discovered_monsters:
                    self.discovered_monsters.append(monster)
                return monster
        
        return None
    
    def remove_monster(self, monster: Monster) -> None:
        """
        Remove a defeated monster from the board.
        
        Args:
            monster: Monster to remove
        """
        if monster in self.monsters:
            self.monsters.remove(monster)
        if monster in self.discovered_monsters:
            self.discovered_monsters.remove(monster)
    
    def get_live_monsters_count(self) -> int:
        """
        Count remaining live monsters.
        
        Returns:
            Number of monsters still alive
        """
        return sum(1 for m in self.monsters if m.is_alive())
    
    def render(self) -> str:
        """
        Render the game board as a string.
        
        Display:
        - 'H' for hero
        - 'L', 'O', 'D' for discovered monsters (Wolf, Orc, Dragonlet)
        - '?' for undiscovered monsters
        - '.' for empty cells
        
        Returns:
            Multi-line string representation of board
        """
        grid = [["." for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        
        # Place undiscovered monsters
        for monster in self.monsters:
            if monster.is_alive() and monster not in self.discovered_monsters:
                grid[monster.y][monster.x] = "?"
        
        # Place discovered monsters
        for monster in self.discovered_monsters:
            if monster.is_alive():
                grid[monster.y][monster.x] = monster.get_symbol()
        
        # Place hero
        if self.hero:
            grid[self.hero.y][self.hero.x] = self.hero.get_symbol()
        
        # Convert to string
        lines = ["+" + "-" * self.WIDTH + "+"]
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append("+" + "-" * self.WIDTH + "+")
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return (
            f"Board("
            f"hero={self.hero.name if self.hero else 'None'}, "
            f"monsters={len(self.monsters)}, "
            f"discovered={len(self.discovered_monsters)}"
            f")"
        )


class Game:
    """
    Main game controller for Heroes vs Monsters.
    
    Manages game flow, combat, and win/loss conditions.
    """
    
    def __init__(self, hero: Hero) -> None:
        """
        Initialize a new game.
        
        Args:
            hero: The hero for this game
        """
        self.hero = hero
        self.board = Board()
        self.board.place_hero(hero, 7, 7)  # Center start position
        
        # Generate and place monsters
        monsters = self._generate_monsters()
        self.board.place_monsters(monsters)
        
        self.turn = 0
        self.game_over = False
        self.victory = False
    
    def _generate_monsters(self) -> List[Monster]:
        """
        Generate random monsters for the board.
        
        Creates 10 monsters with random types.
        
        Returns:
            List of Monster objects
        """
        from v1.monsters import Wolf, Orc, Dragonlet
        
        monsters = []
        monster_types = [Wolf, Orc, Dragonlet]
        
        for _ in range(self.board.NUM_MONSTERS):
            monster_class = random.choice(monster_types)
            monsters.append(monster_class())
        
        return monsters
    
    def attempt_move(self, dx: int, dy: int) -> Tuple[bool, str]:
        """
        Attempt to move the hero.
        
        Args:
            dx: Change in X (-1, 0, or 1)
            dy: Change in Y (-1, 0, or 1)
            
        Returns:
            Tuple of (success, message)
        """
        if not self.hero or self.game_over:
            return False, "Game over or no hero."
        
        new_x = self.hero.x + dx
        new_y = self.hero.y + dy
        
        if not self.board.can_move(new_x, new_y):
            return False, "Cannot move outside the board!"
        
        try:
            adjacent_monster = self.board.move_hero(new_x, new_y)
            
            if adjacent_monster:
                return True, f"Moved to ({new_x}, {new_y}). Combat with {adjacent_monster.name}!"
            else:
                return True, f"Moved to ({new_x}, {new_y})."
        except ValueError as e:
            return False, str(e)
    
    def conduct_combat(self) -> bool:
        """
        Start combat with an adjacent monster.
        
        Returns:
            True if combat occurred, False if no adjacent monster
        """
        monster = self.board.get_adjacent_monster()
        if not monster or not monster.is_alive():
            return False
        
        combat = Combat(self.hero, monster)
        winner = combat.fight_to_death()
        
        print(f"\n{combat.get_log()}\n")
        
        if winner == self.hero:
            # Hero won: collect loot, heal, remove monster
            print(f"Victory! {self.hero.name} defeated {monster.name}!")
            
            loot = monster.generate_loot()
            for item in loot:
                self.hero.add_loot(item)
                print(f"  Collected: {item}")
            
            self.hero.heal_to_full()
            print(f"  {self.hero.name} rests and heals to full HP ({self.hero.max_hp})")
            
            self.board.remove_monster(monster)
        else:
            # Hero died
            print(f"Defeat! {self.hero.name} was killed by {monster.name}!")
            self.game_over = True
        
        return True
    
    def check_win_condition(self) -> bool:
        """
        Check if all monsters are defeated.
        
        Returns:
            True if all monsters are dead
        """
        if self.board.get_live_monsters_count() == 0:
            self.game_over = True
            self.victory = True
            return True
        return False
    
    def check_loss_condition(self) -> bool:
        """
        Check if hero is dead.
        
        Returns:
            True if hero is dead
        """
        if not self.hero.is_alive():
            self.game_over = True
            return True
        return False
    
    def get_status(self) -> str:
        """
        Get current game status.
        
        Returns:
            Multi-line status string with hero info and board
        """
        status_lines = [
            "=" * 30,
            f"Turn: {self.turn}",
            f"Hero: {self.hero}",
            f"Inventory: {self.hero.get_inventory_string()}",
            f"Monsters remaining: {self.board.get_live_monsters_count()}",
            "",
            self.board.render(),
        ]
        return "\n".join(status_lines)
    
    def __repr__(self) -> str:
        return f"Game(hero={self.hero.name}, turn={self.turn})"
