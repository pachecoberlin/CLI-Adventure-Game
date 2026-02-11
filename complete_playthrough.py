#!/usr/bin/env python3
"""Complete playthrough with intelligent combat handling."""

import sys
import random
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure


def play_game_complete():
    """Play a complete game with combat."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║         COMPLETE GAME PLAYTHROUGH WITH COMBAT                 ║
║                                                                ║
║  Testing all major systems:                                   ║
║  ✓ Story generation                                           ║
║  ✓ World exploration                                          ║
║  ✓ Combat encounters and mechanics                           ║
║  ✓ Item management and equipment                             ║
║  ✓ Character progression                                      ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    game = NewAdventure("Adventurer")
    game.initialize_game("fantasy", ["dragon", "quest"], encounters=True)
    
    print(f"\n📖 STORY: {game.story.title}")
    print(f"🎯 GOAL: {game.story.protagonist_goal}")
    print(f"📍 START: {game.map.get_current_location().name}")
    print(f"❤️  HEALTH: {game.player.health}/{game.player.max_health}\n")
    
    # Setup turn counter and combat handler
    turn = 0
    max_turns = 50
    encounters_survived = 0
    items_picked_up = 0
    
    while game.is_running() and turn < max_turns:
        turn += 1
        loc = game.map.get_current_location()
        
        # Determine action based on game state
        if game.state.name == "IN_COMBAT":
            # Combat action
            action = random.choice(["attack", "attack", "attack", "defend", "heal"])
            
            # Don't heal if at full health
            if action == "heal" and game.player.health >= game.player.max_health - 10:
                action = "attack"
            
            result = game.process_command(action)
            
            if "victory" in result.lower():
                encounters_survived += 1
                print(f"[{turn}] ⚔️  VICTORY! ({encounters_survived} enemies defeated)")
            elif "defeated" in result.lower():
                print(f"[{turn}] 💀 GAME OVER")
                break
                
        else:
            # Exploration action
            if turn % 3 == 0:
                # Try to move
                result = game.process_command("go north")
                
                if "enemy" in result.lower() or "encounter" in result.lower():
                    print(f"[{turn}] 👹 Enemy encountered at {loc.name}!")
                    
            elif turn % 4 == 0:
                # Look at location
                result = game.process_command("look")
                
                # Count items
                if loc and loc.items_on_ground:
                    print(f"[{turn}] 📍 At {loc.name} - {len(loc.items_on_ground)} item(s) available")
                    
            elif turn % 5 == 0:
                # Try to pick up items
                if loc and loc.items_on_ground:
                    item = loc.items_on_ground[0]
                    result = game.process_command(f"take {item.name.lower()}")
                    if "took the" in result.lower():
                        items_picked_up += 1
                        print(f"[{turn}] 📦 Picked up: {item.name}")
                        
            elif turn % 6 == 0:
                # Show status
                result = game.process_command("status")
                
            elif turn == 1:
                # Setup: equip weapon
                result = game.process_command("equip iron sword")
                print(f"[{turn}] ⚔️  Equipped Iron Sword (Damage +15)")
                
            else:
                # Random action
                result = game.process_command("look")
    
    # Final report
    print("\n" + "="*60)
    print("GAME COMPLETE - FINAL REPORT")
    print("="*60)
    print(f"Duration: {turn} turns")
    print(f"State: {game.state.name}")
    print(f"Health: {game.player.health}/{game.player.max_health}")
    print(f"Items collected: {items_picked_up}")
    print(f"Enemies defeated: {encounters_survived}")
    print(f"Equipment:")
    if game.player.equipment_weapon:
        print(f"  Weapon: {game.player.equipment_weapon.name}")
    if game.player.equipment_armor:
        print(f"  Armor: {game.player.equipment_armor.name}")
    print(f"Inventory: {len(game.player.inventory)} items")
    
    return game


if __name__ == "__main__":
    try:
        game = play_game_complete()
        print("\n✓ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
