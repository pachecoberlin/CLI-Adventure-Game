#!/usr/bin/env python3
"""Full playthrough test of the adventure game."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure


def simulate_game_run(genre, keywords):
    """Simulate a full game run."""
    print(f"\n{'='*70}")
    print(f"FULL GAME PLAYTHROUGH TEST: {genre.upper()}")
    print(f"Keywords: {keywords}")
    print(f"{'='*70}\n")
    
    # Initialize game
    game = NewAdventure("TestPlayer")
    game.initialize_game(genre, keywords, encounters=True)
    
    print(f"✓ Game initialized")
    print(f"  Story: {game.story.title}")
    print(f"  Goal: {game.story.protagonist_goal}")
    print(f"  Starting location: {game.map.get_current_location().name}")
    print(f"  Health: {game.player.health}/{game.player.max_health}")
    print(f"  Inventory: {len(game.player.inventory)} items\n")
    
    turn_limit = 50
    turn_count = 0
    
    # Simulate game commands
    commands_to_try = [
        "look",
        "inventory",
        "status",
        "story",
        "go north",
        "look",
        "go north",
        "look",
        "inventory",
        "help",
    ]
    
    print("GAME ACTIONS:")
    for cmd in commands_to_try:
        if turn_count >= turn_limit:
            print(f"\n⚠ Reached turn limit ({turn_limit})")
            break
        
        if not game.is_running():
            print(f"\n✓ Game ended at turn {game.turn_count}")
            print(f"  State: {game.state.name}")
            break
        
        try:
            response = game.process_command(cmd)
            # Truncate for display
            display = response[:100] + "..." if len(response) > 100 else response
            print(f"  [{game.turn_count}] ➜ {cmd}")
            print(f"       {display}\n")
            turn_count += 1
            
        except Exception as e:
            print(f"  ERROR: {e}")
            break
    
    print(f"\n✓ Test complete!")
    print(f"  Total turns: {game.turn_count}")
    print(f"  Final state: {game.state.name}")
    print(f"  Final health: {game.player.health}/{game.player.max_health}")
    
    return game


def main():
    """Run tests for all genres."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║             FULL PLAYTHROUGH TEST - ALL GENRES                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    genres = [
        ("fantasy", ["dragon", "curse"]),
        ("scifi", ["space", "station"]),
        ("detective", ["murder", "clues"]),
        ("horror", ["haunted", "dark"]),
    ]
    
    for genre, keywords in genres:
        try:
            game = simulate_game_run(genre, keywords)
        except Exception as e:
            print(f"\n❌ Test failed for {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("✓ ALL PLAYTHROUGH TESTS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
