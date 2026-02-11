#!/usr/bin/env python3
"""Automated game playthrough for testing."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure


def automated_game():
    """Play through a complete game automatically."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║              AUTOMATED GAME PLAYTHROUGH TEST                  ║
║                                                                ║
║  This test plays through a complete game, handling:           ║
║  - World exploration                                          ║
║  - Combat encounters                                          ║
║  - Item management                                            ║
║  - Story progression                                          ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize game
    game = NewAdventure("TestHero")
    game.initialize_game("fantasy", ["dragon", "treasure", "ancient"], encounters=True)
    
    print(f"\n✓ Game started!")
    print(f"  Story: {game.story.title}")
    print(f"  Goal: {game.story.protagonist_goal}")
    print(f"  Starting health: {game.player.health}/{game.player.max_health}\n")
    
    # Define a sequence of commands to execute
    game_plan = [
        ("look", "Examine starting location"),
        ("inventory", "Check starting inventory"),
        ("equip iron sword", "Equip weapon"),
        ("status", "Check character status"),
        ("story", "Check story progress"),
    ]
    
    # Exploration phase
    for i in range(15):
        if not game.is_running():
            break
        game_plan.append(("go north", f"Explore north (turn {game.turn_count})"))
    
    # Execute game plan
    print("EXECUTING GAME PLAN:")
    print("="*60)
    
    for cmd, description in game_plan:
        if not game.is_running():
            print(f"\n✓ Game ended at turn {game.turn_count}")
            break
        
        try:
            response = game.process_command(cmd)
            
            # Check for important events
            if "victory" in response.lower() or "defeated" in response.lower():
                print(f"\n[{game.turn_count}] ⚔️  {description}")
                print(f"  Command: {cmd}")
                print(f"  Result: {response[:120]}...\n")
            elif "encounter" in response.lower() or "enemy" in response.lower():
                print(f"[{game.turn_count}] 👹 {description}")
                print(f"  Encountered enemy in combat!\n")
            elif "took the" in response.lower():
                item_name = response.split("took the ")[1].split(".")[0]
                print(f"[{game.turn_count}] 📦 Found item: {item_name}")
            elif game.turn_count % 5 == 0:
                print(f"[{game.turn_count}] ✓ {description}")
                
        except Exception as e:
            print(f"\n[ERROR] Turn {game.turn_count}: {e}")
            break
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL GAME SUMMARY")
    print("="*60)
    print(f"Game State: {game.state.name}")
    print(f"Total Turns: {game.turn_count}")
    print(f"Final Health: {game.player.health}/{game.player.max_health}")
    print(f"Equipment:")
    print(f"  Weapon: {game.player.equipment_weapon.name if game.player.equipment_weapon else 'None'}")
    print(f"  Armor: {game.player.equipment_armor.name if game.player.equipment_armor else 'None'}")
    print(f"  Damage Bonus: +{game.player.get_total_damage_bonus()}")
    print(f"  Armor Value: {game.player.get_total_armor()}")
    print(f"Inventory ({len(game.player.inventory)} items):")
    for item in game.player.inventory:
        print(f"  - {item.name}: {item.description}")
    
    print("\n✓ Automated playthrough complete!")
    return True


if __name__ == "__main__":
    try:
        success = automated_game()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Playthrough failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
