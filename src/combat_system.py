"""Multi-round combat system with defense, attack, heal, and flee."""

from typing import Optional, Dict
from dataclasses import dataclass, field
import random
from enum import Enum


class CombatAction(Enum):
    """Possible actions in combat."""
    ATTACK = "attack"
    DEFEND = "defend"
    HEAL = "heal"
    FLEE = "flee"
    SPECIAL = "special"


@dataclass
class Enemy:
    """An enemy in combat."""
    name: str
    health: int
    max_health: int
    damage: int
    armor: int = 0
    special_ability: Optional[str] = None


@dataclass
class CombatRound:
    """A single round of combat."""
    round_number: int
    player_action: CombatAction
    player_action_detail: str  # e.g., item name for heal/attack
    enemy_action: str
    player_damage_dealt: int
    player_damage_taken: int
    combat_log: str


class CombatSystem:
    """Manages combat encounters."""
    
    def __init__(self, player_health: int, player_armor: int = 0):
        self.player_health = player_health
        self.max_player_health = player_health
        self.player_armor = player_armor
        self.enemy: Optional[Enemy] = None
        self.rounds: list[CombatRound] = []
        self.is_active = False
    
    def start_encounter(self, enemy: Enemy):
        """Start a new combat encounter."""
        self.enemy = enemy
        self.is_active = True
        self.rounds = []
    
    def calculate_damage(self, base_damage: int, defender_armor: int = 0) -> int:
        """Calculate actual damage after armor reduction."""
        # Armor reduces damage (each point of armor = 1 damage reduction)
        actual_damage = max(1, base_damage - defender_armor)
        # Add some variance (±20%)
        variance = int(actual_damage * 0.2)
        actual_damage += random.randint(-variance, variance)
        return max(1, actual_damage)
    
    def execute_action(self, action: CombatAction, detail: str = "") -> Dict:
        """Execute a player action in combat."""
        
        if not self.is_active or not self.enemy:
            return {"success": False, "message": "No active combat."}
        
        round_num = len(self.rounds) + 1
        log = f"Round {round_num}:\n"
        
        player_damage = 0
        player_takes_damage = 0
        enemy_action_text = ""
        
        # Process player action
        if action == CombatAction.ATTACK:
            player_damage = self.calculate_damage(10)  # Base damage
            log += f"  You attack! Dealing {player_damage} damage.\n"
            self.enemy.health -= player_damage
        
        elif action == CombatAction.DEFEND:
            self.player_armor += 5  # Temporary armor boost
            log += f"  You brace for impact! (+5 armor this round)\n"
        
        elif action == CombatAction.HEAL:
            if detail:  # detail = healing amount
                heal_amount = int(detail)
                self.player_health = min(self.max_player_health, self.player_health + heal_amount)
                log += f"  You use a healing item! Restored {heal_amount} HP.\n"
        
        elif action == CombatAction.FLEE:
            if random.random() < 0.6:  # 60% flee chance
                log += f"  You manage to escape!\n"
                self.is_active = False
                return {"success": True, "message": log, "fled": True}
            else:
                log += f"  You can't escape!\n"
        
        # Enemy's turn
        if self.is_active and self.enemy.health > 0:
            enemy_damage = self.calculate_damage(self.enemy.damage, self.player_armor)
            self.player_health -= enemy_damage
            enemy_action_text = f"  {self.enemy.name} attacks! Dealing {enemy_damage} damage.\n"
            log += enemy_action_text
            player_takes_damage = enemy_damage
            
            # Reduce temporary armor after use
            if self.player_armor > 0 and action == CombatAction.DEFEND:
                self.player_armor -= 5
        
        # Check if combat is over
        if self.enemy.health <= 0:
            self.is_active = False
            log += f"\nVICTORY! You defeated the {self.enemy.name}!"
            return {"success": True, "message": log, "victory": True}
        
        if self.player_health <= 0:
            self.is_active = False
            log += f"\nDEFEAT! You were defeated."
            return {"success": True, "message": log, "defeat": True}
        
        # Combat continues
        round_info = CombatRound(
            round_number=round_num,
            player_action=action,
            player_action_detail=detail,
            enemy_action=enemy_action_text,
            player_damage_dealt=player_damage,
            player_damage_taken=player_takes_damage,
            combat_log=log
        )
        self.rounds.append(round_info)
        
        status = f"Your Health: {self.player_health}/{self.max_player_health} | {self.enemy.name} Health: {self.enemy.health}/{self.enemy.max_health}"
        
        return {
            "success": True,
            "message": log,
            "status": status,
            "combat_active": True,
        }
    
    def get_available_actions(self, inventory_items: list) -> Dict:
        """Get available combat actions."""
        actions = {
            "attack": "Attack the enemy",
            "defend": "Defend to reduce damage this round",
            "flee": "Try to escape from combat",
        }
        
        # Add heal if healing items available
        healing_items = [item for item in inventory_items if hasattr(item, 'healing_amount') and item.healing_amount > 0]
        if healing_items:
            for item in healing_items:
                actions[f"heal_with_{item.name.lower().replace(' ', '_')}"] = f"Use {item.name} ({item.healing_amount} HP)"
        
        return actions
