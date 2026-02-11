#!/usr/bin/env python3
"""Test complete game from start to victory."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure, GameState
from src.item_system import Item, ItemType


def complete_victory_run():
    """Play a complete game from start to victory."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║               COMPLETE VICTORY RUN TEST                       ║
║                                                                ║
║  This test verifies the complete game loop:                   ║
║  ✓ Game initialization                                        ║
║  ✓ Story generation                                           ║
║  ✓ Exploration and item collection                           ║
║  ✓ Combat encounters and progression                         ║
║  ✓ Boss encounter and story completion                       ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Create and initialize game
    game = NewAdventure("VictorySeeker")
    game.initialize_game("fantasy", ["dragon", "ancient", "curse"], encounters=True)
    
    print(f"\n📖 STORY: {game.story.title}")
    print(f"🎯 GOAL: {game.story.protagonist_goal}")
    print(f"📍 START: {game.map.get_current_location().name}")
    print(f"❤️  HEALTH: {game.player.health}/{game.player.max_health}\n")
    
    # Add lots of healing for boss fight
    for i in range(15):
        game.player.inventory.append(
            Item("Health Potion", "Restores 30 HP", ItemType.HEALING, 
                 healing_amount=30, is_consumable=True)
        )
    
    # Equip weapon
    game.player.equipment_weapon = game.player.inventory[2]  # Iron Sword
    
    print("="*60)
    print("GAME PROGRESSION")
    print("="*60)
    
    exploration_phase = True
    encounters = 0
    victories = 0
    
    while game.state == GameState.EXPLORING:
        if game.turn_count > 100:
            print("⚠ Reached turn limit")
            break
        
        # Alternate between exploration and combat
        if game.state == GameState.IN_COMBAT:
            # Combat handling
            if game.player.health < 50 and game.turn_count % 2 == 0:
                result = game.cmd_heal('')
            else:
                result = game.cmd_attack('')
            
            if "VICTORY" in result:
                if game.state == GameState.VICTORY:
                    print(f"\n[{game.turn_count}] 🏆 BOSS DEFEATED - STORY VICTORY!")
                    break
                else:
                    victories += 1
        else:
            # Exploration
            if game.turn_count % 4 == 0:
                result = game.process_command("go north")
                if "enemy" in result.lower():
                    encounters += 1
                    print(f"[{game.turn_count}] ⚔️  Combat encounter #{encounters}")
            elif game.turn_count % 5 == 0:
                game.process_command("look")
            else:
                game.process_command("inventory")
        
        # Force boss at later turns
        if game.turn_count > 40 and game.state == GameState.EXPLORING and game.turn_count % 8 == 0:
            # Manually create boss encounter
            from src.combat_system import Enemy, CombatSystem
            boss_name = game.story.protagonist_goal.split("Stop ")[1].split(" ")[0] if "Stop " in game.story.protagonist_goal else "Dragon"
            
            boss = Enemy(boss_name, 80, 80, 15, 5)
            game.combat_system = CombatSystem(game.player.health, game.player.get_total_armor())
            game.combat_system.start_encounter(boss)
            game.state = GameState.IN_COMBAT
            
            print(f"\n[{game.turn_count}] ⚠️  BOSS ENCOUNTER: {boss_name}!")
    
    # Show results
    print("\n" + "="*60)
    print("VICTORY!")
    print("="*60)
    print(f"Game State: {game.state.name}")
    print(f"Total Turns: {game.turn_count}")
    print(f"Total Encounters: {encounters}")
    print(f"Final Health: {game.player.health}/{game.player.max_health}")
    print(f"Items in Inventory: {len(game.player.inventory)}")
    
    # Show ending
    if game.state == GameState.VICTORY:
        print("\n✓ GAME COMPLETED WITH STORY VICTORY!")
        return True
    else:
        print(f"\n⚠ Game ended in state: {game.state.name}")
        return False


if __name__ == "__main__":
    try:
        success = complete_victory_run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
