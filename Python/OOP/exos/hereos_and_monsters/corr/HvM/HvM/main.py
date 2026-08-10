"""
Heroes vs Monsters - Main game entry point.

Run this file to start playing the game.
"""

import os
import sys
from v1.heroes import Human, Dwarf
from v1.game import Game


def clear_screen() -> None:
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_title() -> None:
    """Print the game title and welcome message."""
    clear_screen()
    print("""
    ╔════════════════════════════════════════╗
    ║     HEROES vs MONSTERS                 ║
    ║     Forêt de Shorewood                 ║
    ║     Stormwall                          ║
    ╚════════════════════════════════════════╝
    """)


def choose_hero() -> tuple:
    """
    Let player choose hero type and name.
    
    Returns:
        Tuple of (hero_class, hero_name)
    """
    print_title()
    print("Welcome to Shorewood Forest!\n")
    print("Choose your hero:\n")
    print("1. Human  [+1 Strength, +1 Endurance]")
    print("2. Dwarf  [+2 Endurance]\n")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == "1":
            hero_class = Human
            break
        elif choice == "2":
            hero_class = Dwarf
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    hero_name = input("\nEnter your hero's name: ").strip()
    if not hero_name:
        hero_name = "Hero"
    
    return hero_class, hero_name


def print_controls() -> None:
    """Print game controls help."""
    print("""
    ╔════════════════════════════════════════╗
    ║           GAME CONTROLS                ║
    ╠════════════════════════════════════════╣
    ║  Z/↑  - Move North                     ║
    ║  S/↓  - Move South                     ║
    ║  Q/←  - Move West                      ║
    ║  D/→  - Move East                      ║
    ║  C    - Conduct Combat (auto-trigger)  ║
    ║  H    - Show this help                 ║
    ║  QUIT - Exit game                      ║
    ╠════════════════════════════════════════╣
    ║  H = Hero | L = Wolf | O = Orc         ║
    ║  D = Dragonlet | ? = Hidden Monster    ║
    ║  . = Empty Cell                        ║
    ╚════════════════════════════════════════╝
    """)


def get_player_input() -> str:
    """
    Get and validate player input.
    
    Returns:
        Lowercase command string
    """
    while True:
        command = input("\n> ").strip().lower()
        if command:
            return command
        print("Please enter a command.")


def process_input(game: Game, command: str) -> bool:
    """
    Process player input and update game state.
    
    Args:
        game: Current Game instance
        command: Player command
        
    Returns:
        True if game should continue, False if player quit
    """
    move_map = {
        "z": (0, -1),
        "↑": (0, -1),
        "arrowup": (0, -1),
        "s": (0, 1),
        "↓": (0, 1),
        "arrowdown": (0, 1),
        "q": (-1, 0),
        "←": (-1, 0),
        "arrowleft": (-1, 0),
        "d": (1, 0),
        "→": (1, 0),
        "arrowright": (1, 0),
    }
    
    if command in move_map:
        dx, dy = move_map[command]
        success, message = game.attempt_move(dx, dy)
        print(message)
        
        if success and not game.game_over:
            game.turn += 1
            # Attempt combat if adjacent
            game.conduct_combat()
            
            # Check win condition
            if game.check_win_condition():
                print_victory(game)
                return False
            
            # Check loss condition
            if game.check_loss_condition():
                print_defeat(game)
                return False
    
    elif command == "c":
        if game.conduct_combat():
            game.turn += 1
            
            if game.check_win_condition():
                print_victory(game)
                return False
            
            if game.check_loss_condition():
                print_defeat(game)
                return False
        else:
            print("No monster adjacent to fight!")
    
    elif command == "h":
        print_controls()
    
    elif command == "quit" or command == "exit":
        print("\nThanks for playing! Goodbye!")
        return False
    
    else:
        print("Unknown command. Press 'h' for help.")
    
    return True


def print_game_state(game: Game) -> None:
    """
    Print current game state.
    
    Args:
        game: Current Game instance
    """
    print("\n" + game.get_status())


def print_victory(game: Game) -> None:
    """
    Print victory screen.
    
    Args:
        game: Completed Game instance
    """
    print("""
    ╔════════════════════════════════════════╗
    ║           VICTORY!                     ║
    ╚════════════════════════════════════════╝
    """)
    print(f"{game.hero.name} has conquered Shorewood Forest!")
    print(f"\nFinal Stats:")
    print(f"  HP: {game.hero.hp}/{game.hero.max_hp}")
    print(f"  Turns: {game.turn}")
    print(f"  {game.hero.get_inventory_string()}")
    print(f"\nAll monsters defeated. You are victorious!\n")


def print_defeat(game: Game) -> None:
    """
    Print defeat screen.
    
    Args:
        game: Completed Game instance
    """
    print("""
    ╔════════════════════════════════════════╗
    ║           DEFEAT!                      ║
    ╚════════════════════════════════════════╝
    """)
    print(f"{game.hero.name} has fallen in Shorewood Forest...")
    print(f"\nFinal Stats:")
    print(f"  HP: {game.hero.hp}/{game.hero.max_hp}")
    print(f"  Turns: {game.turn}")
    print(f"  {game.hero.get_inventory_string()}")
    print(f"\nYou were defeated. Better luck next time!\n")


def main() -> None:
    """Main game loop."""
    hero_class, hero_name = choose_hero()
    hero = hero_class(hero_name)
    
    game = Game(hero)
    
    print_title()
    print(f"Welcome, {hero.name}!")
    print(f"You are a {hero.__class__.__name__}.")
    print(f"Stats: Strength={hero.strength}, Endurance={hero.endurance}, HP={hero.max_hp}\n")
    print_controls()
    
    print_game_state(game)
    
    # Main game loop
    while not game.game_over:
        command = get_player_input()
        if not process_input(game, command):
            break
        
        if not game.game_over:
            print_game_state(game)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
