#!/usr/bin/env python3
"""Full game playthrough test - exploring, combat, items, etc."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure


def full_playthrough():
    """Simulate a complete game playthrough."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    FULL GAME PLAYTHROUGH TEST                 ║
║            Complete exploration, combat, and items            ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    game = NewAdventure("Adventurer")
    game.initialize_game("fantasy", ["dragon", "treasure", "curse"], encounters=True)
    
    print(f"✓ Game initialized")
    print(f"  Title: {game.story.title}")
    print(f"  Goal: {game.story.protagonist_goal}")
    print(f"  Locations: {len(game.story.locations)}\n")
    
    # Simulate gameplay
    turn_limit = 100
    locations_visited = set()
    combat_count = 0
    items_found = 0
    
    # Starting commands
    commands = [
        "look",
        "inventory",
        "equip iron sword",
        "status",
    ]
    
    # Exploration and combat loop
    for turn in range(turn_limit):
        if not game.is_running():
            print(f"\n[END] Game stopped at turn {turn}")
            break
        
        loc = game.map.get_current_location()
        if loc:
            locations_visited.add(loc.name)
        
        # Choose next action based on state
        if game.state.name == "IN_COMBAT":
            # Combat action
            combat_actions = ["attack", "defend", "heal"]
            action = combat_actions[turn % len(combat_actions)]
            commands.append(action)
        else:
            # Exploration action
            if turn > 30 and turn % 5 == 0:
                commands.append("go north")
            elif turn % 15 == 0:
                commands.append("look")
            elif turn % 20 == 0:
                commands.append("inventory")
            else:
                # Try to take items
                if loc and loc.items_on_ground:
                    item_name = loc.items_on_ground[0].name.lower()
                    commands.append(f"take {item_name}")
        
        if not commands:
            break
        
        cmd = commands.pop(0)
        try:
            result = game.process_command(cmd)
            
            # Track events
            if "victory" in result.lower() or "defeated" in result.lower():
                combat_count += 1
            if "took the" in result.lower():
                items_found += 1
            
            # Show occasional updates
            if game.turn_count % 15 == 0:
                print(f"[Turn {game.turn_count}] {cmd}")
                print(f"  State: {game.state.name}")
                print(f"  Health: {game.player.health}/{game.player.max_health}")
                print(f"  Inventory: {len(game.player.inventory)} items")
                print(f"  Locations: {len(locations_visited)}")
                
        except Exception as e:
            print(f"\n[ERROR] Turn {game.turn_count}: {e}")
            break
    
    # Final report
    print(f"\n{'='*60}")
    print("FINAL REPORT")
    print(f"{'='*60}")
    print(f"Game State: {game.state.name}")
    print(f"Final Health: {game.player.health}/{game.player.max_health}")
    print(f"Total Turns: {game.turn_count}")
    print(f"Locations Visited: {len(locations_visited)}")
    print(f"Items Collected: {len(game.player.inventory)}")
    print(f"Inventory: {[item.name for item in game.player.inventory]}")
    print(f"Damage Bonus: +{game.player.get_total_damage_bonus()}")
    print(f"Armor: {game.player.get_total_armor()}")
    
    return game


if __name__ == "__main__":
    try:
        game = full_playthrough()
        print(f"\n✓ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
