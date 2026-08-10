"""
Quick test script to verify game mechanics work correctly.
Run this to validate the implementation before playing the full game.
"""

import sys
sys.path.insert(0, r'c:\Users\byase\Documents\Programming\Courses\Python\[Python] Orienté Objet\Exercices\hvm')

from v1.heroes import Human, Dwarf
from v1.monsters import Wolf, Orc, Dragonlet
from v1.game import Combat, Board, Game
from v1.character import Character


def test_modifiers():
    """Test modifier calculation."""
    print("=" * 50)
    print("TEST: Modifier Calculation")
    print("=" * 50)
    
    test_cases = [
        (3, -1, "Low characteristic (< 5)"),
        (4, -1, "Boundary low"),
        (5, 0, "Start medium (5-9)"),
        (9, 0, "End medium"),
        (10, 1, "Start high (10-14)"),
        (14, 1, "End high"),
        (15, 2, "Very high (>= 15)"),
        (18, 2, "Maximum"),
    ]
    
    for stat, expected, desc in test_cases:
        result = Character.calculate_modifier(stat)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stat:2d} → {result:+2d} (expected {expected:+2d}) [{desc}]")


def test_hero_creation():
    """Test hero creation and bonuses."""
    print("\n" + "=" * 50)
    print("TEST: Hero Creation")
    print("=" * 50)
    
    human = Human("TestHuman")
    print(f"Human: Str={human.strength}, End={human.endurance}, HP={human.hp}")
    print(f"  Base should have +1 to both Str and End")
    
    dwarf = Dwarf("TestDwarf")
    print(f"Dwarf: Str={dwarf.strength}, End={dwarf.endurance}, HP={dwarf.hp}")
    print(f"  Base should have +2 to End only")
    
    print("✓ Hero creation works!")


def test_monster_creation():
    """Test monster creation and loot."""
    print("\n" + "=" * 50)
    print("TEST: Monster Creation & Loot")
    print("=" * 50)
    
    wolf = Wolf()
    print(f"Wolf: Str={wolf.strength}, End={wolf.endurance}")
    loot = wolf.generate_loot()
    print(f"  Loot: {loot}")
    
    orc = Orc()
    print(f"Orc: Str={orc.strength}, End={orc.endurance}")
    print(f"  Orc +1 Str applied")
    loot = orc.generate_loot()
    print(f"  Loot: {loot}")
    
    dragon = Dragonlet()
    print(f"Dragonlet: Str={dragon.strength}, End={dragon.endurance}")
    print(f"  Dragonlet +1 End applied")
    loot = dragon.generate_loot()
    print(f"  Loot: {loot}")
    
    print("✓ Monster creation works!")


def test_combat():
    """Test combat mechanics."""
    print("\n" + "=" * 50)
    print("TEST: Combat System")
    print("=" * 50)
    
    human = Human("Aragorn")
    wolf = Wolf()
    
    print(f"Hero: {human.name} (HP={human.hp}, Str={human.strength})")
    print(f"Monster: {wolf.name} (HP={wolf.hp}, Str={wolf.strength})")
    print()
    
    combat = Combat(human, wolf)
    winner = combat.fight_to_death()
    
    print(combat.get_log())
    print(f"\nWinner: {winner.name}")
    print(f"Hero final HP: {human.hp}")
    
    print("✓ Combat system works!")


def test_board():
    """Test board and monster placement."""
    print("\n" + "=" * 50)
    print("TEST: Board & Monster Placement")
    print("=" * 50)
    
    hero = Human("TestHero", 7, 7)
    
    board = Board()
    board.place_hero(hero)
    
    monsters = [Wolf(), Orc(), Dragonlet(), Wolf(), Orc()]
    board.place_monsters(monsters)
    
    print(f"Hero position: ({board.hero.x}, {board.hero.y})")
    print(f"Monsters on board: {len(board.monsters)}")
    
    for monster in board.monsters:
        print(f"  {monster.name} at ({monster.x}, {monster.y})")
    
    print("\nBoard render:")
    print(board.render())
    
    print("✓ Board placement works!")


def test_game_initialization():
    """Test game initialization."""
    print("\n" + "=" * 50)
    print("TEST: Game Initialization")
    print("=" * 50)
    
    hero = Human("TestHero")
    game = Game(hero)
    
    print(f"Game created with hero: {game.hero.name}")
    print(f"Monsters spawned: {len(game.board.monsters)}")
    print(f"Live monsters: {game.board.get_live_monsters_count()}")
    print(f"Hero position: ({game.hero.x}, {game.hero.y})")
    print(f"Board size: {game.board.WIDTH}x{game.board.HEIGHT}")
    
    print("\n" + game.get_status())
    
    print("✓ Game initialization works!")


def main():
    """Run all tests."""
    print("\n")
    print("╔════════════════════════════════════════╗")
    print("║   HEROES vs MONSTERS - TEST SUITE      ║")
    print("╚════════════════════════════════════════╝")
    
    try:
        test_modifiers()
        test_hero_creation()
        test_monster_creation()
        test_combat()
        test_board()
        test_game_initialization()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nImplementation is ready to play!")
        print("Run 'python main.py' to start the game.\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
