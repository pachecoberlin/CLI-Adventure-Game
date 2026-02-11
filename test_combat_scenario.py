#!/usr/bin/env python3
"""Test combat scenario in game."""

import sys
sys.path.insert(0, '/tmp/CLI-Adventure-Game')

from src.new_game_engine import NewAdventure


def test_combat_scenario():
    """Test a full combat scenario."""
    print("="*70)
    print("COMBAT SCENARIO TEST")
    print("="*70)
    
    game = NewAdventure("CombatTester")
    game.initialize_game("fantasy", ["dragon", "battle"], encounters=True)
    
    print(f"✓ Game started")
    print(f"  Health: {game.player.health}/{game.player.max_health}")
    print(f"  Inventory: {[item.name for item in game.player.inventory]}\n")
    
    # Equip weapon
    print("1. Equipping weapon...")
    result = game.process_command("equip iron sword")
    print(f"   {result}\n")
    
    print(f"   Damage bonus: {game.player.get_total_damage_bonus()}")
    
    # Move and trigger encounter
    print("\n2. Moving north (trying to trigger encounter)...")
    for i in range(10):
        if game.state.name == "IN_COMBAT":
            print(f"   ✓ Combat started!")
            break
        result = game.process_command("go north")
        print(f"   Turn {game.turn_count}: {'ENCOUNTER!' if 'enemy' in result.lower() else 'Safe'}")
    
    if game.state.name != "IN_COMBAT":
        print("\n   ⚠ No combat triggered, manually starting...")
        game.start_encounter()
    
    # Combat actions
    print(f"\n3. Combat Actions (State: {game.state.name}):")
    print(f"   Health: {game.player.health}/{game.player.max_health}")
    print(f"   Combat active: {game.state.name == 'IN_COMBAT'}\n")
    
    combat_commands = [
        "attack",
        "attack",
        "defend",
        "attack",
        "heal",
        "attack",
    ]
    
    for cmd in combat_commands:
        if not game.is_running() or game.state.name == "VICTORY" or game.state.name == "DEFEAT":
            print(f"\n   Game ended (state: {game.state.name})")
            break
        
        result = game.process_command(cmd)
        print(f"   [{game.turn_count}] {cmd}: {result[:80]}...")
    
    print(f"\n✓ Combat test complete!")
    print(f"  Final state: {game.state.name}")
    print(f"  Final health: {game.player.health}/{game.player.max_health}")


if __name__ == "__main__":
    try:
        test_combat_scenario()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
