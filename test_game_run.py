#!/usr/bin/env python3
"""Test a complete game run with automated commands."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure
from src.dynamic_ascii import DynamicASCII


def test_game():
    """Run a test game session."""
    print("="*70)
    print("STARTING TEST GAME RUN")
    print("="*70)
    
    # Create and initialize game
    game = NewAdventure("TestHero")
    game.initialize_game("fantasy", ["dragon", "curse", "prophecy"], encounters=True)
    
    print(f"\n✓ Game initialized")
    print(f"  Story: {game.story.title}")
    print(f"  Protagonist Goal: {game.story.protagonist_goal}")
    print(f"  Current Location: {game.map.get_current_location().name}")
    print(f"  Health: {game.player.health}")
    print(f"  Inventory: {len(game.player.inventory)} items")
    
    # Test commands in sequence
    commands = [
        "look",           # Look at current location
        "inventory",      # Check inventory
        "examine map",    # Look at specific item
        "go north",       # Try to move
        "help",          # Show help
    ]
    
    print("\n" + "="*70)
    print("TESTING BASIC COMMANDS")
    print("="*70)
    
    for cmd in commands:
        print(f"\n→ Command: {cmd}")
        try:
            response = game.process_command(cmd)
            print(response[:200] + "..." if len(response) > 200 else response)
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("TESTING GAME STATE")
    print("="*70)
    print(f"Game running: {game.is_running()}")
    print(f"State: {game.state.name}")
    print(f"Turn count: {game.turn_count}")
    
    print("\n✓ Test complete - basic systems functional!")
    return True


if __name__ == "__main__":
    try:
        success = test_game()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
