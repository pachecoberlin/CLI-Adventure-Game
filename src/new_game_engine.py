"""Complete rewritten game engine with story, map, items, NPCs, and combat."""

import random
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

from src.story_generator import StoryGenerator, Story
from src.map_system import Map, Location, LocationDescription, Transition, TransitionType, InspectableObject
from src.item_system import Item, ItemType, ItemFactory
from src.npc_system import NPC, NPCFactory, NPCInteraction
from src.combat_system import CombatSystem, Enemy, CombatAction
from src.dynamic_ascii import DynamicASCII


class GameState(Enum):
    """Game states."""
    STARTING = "starting"
    EXPLORING = "exploring"
    IN_COMBAT = "in_combat"
    VICTORY = "victory"
    DEFEAT = "defeat"
    QUIT = "quit"


@dataclass
class PlayerCharacter:
    """The player character."""
    name: str
    health: int = 100
    max_health: int = 100
    inventory: List[Item] = None
    equipment_weapon: Optional[Item] = None
    equipment_armor: Optional[Item] = None
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
    
    def get_total_damage_bonus(self) -> int:
        """Get total damage bonus from equipment."""
        bonus = 0
        if self.equipment_weapon and hasattr(self.equipment_weapon, 'damage_bonus'):
            bonus += self.equipment_weapon.damage_bonus
        return bonus
    
    def get_total_armor(self) -> int:
        """Get total armor value from equipment."""
        armor = 0
        if self.equipment_armor and hasattr(self.equipment_armor, 'armor_value'):
            armor += self.equipment_armor.armor_value
        return armor


class NewAdventure:
    """Complete rewritten adventure game."""
    
    def __init__(self, player_name: str):
        self.player = PlayerCharacter(name=player_name)
        self.story: Optional[Story] = None
        self.map: Optional[Map] = None
        self.state = GameState.STARTING
        self.turn_count = 0
        self.encounters_enabled = False
        self.combat_system: Optional[CombatSystem] = None
        self.current_story_node = None
        self.game_log: List[str] = []
    
    def initialize_game(self, genre: str, keywords: List[str], encounters: bool):
        """Initialize a new game with story and world."""
        self.encounters_enabled = encounters
        
        # Generate story
        self.story = StoryGenerator.generate_story(genre, keywords, self.player.name)
        
        # Generate and set up world
        self._setup_world(genre)
        
        # Add starting items
        self._add_starting_items(genre)
        
        # Start game
        self.state = GameState.EXPLORING
        self.current_story_node = self.story.start_node
    
    def _setup_world(self, genre: str):
        """Setup the game world."""
        self.map = Map()
        
        # Create locations from story
        for i, location_name in enumerate(self.story.locations):
            loc = Location(
                id=f"loc_{i}",
                name=location_name,
                descriptions=LocationDescription(
                    first_time=f"You arrive at {location_name}.",
                    revisit_short=f"You're back at {location_name}.",
                    detailed=f"You examine {location_name} carefully...",
                ),
            )
            self.map.add_location(loc)
        
        # Setup connections between locations
        locations_list = list(self.map.locations.values())
        for i, loc in enumerate(locations_list):
            next_idx = (i + 1) % len(locations_list)
            next_loc = locations_list[next_idx]
            loc.transitions["north"] = Transition(
                destination=next_loc.id,
                description=f"You travel north to {next_loc.name}.",
            )
        
        # Place items in random locations
        weapons = ItemFactory.get_weapons(genre)
        armor = ItemFactory.get_armor(genre)
        healing = ItemFactory.get_healing_items()
        
        for loc in locations_list[1:]:  # Skip starting location
            if random.random() < 0.5 and weapons:
                loc.items_on_ground.append(random.choice(weapons))
            if random.random() < 0.4 and armor:
                loc.items_on_ground.append(random.choice(armor))
            if random.random() < 0.6 and healing:
                loc.items_on_ground.append(random.choice(healing))
        
        # Place NPCs in random locations
        npc_templates = NPCFactory.get_npcs(genre)
        for loc in locations_list[1:]:  # Skip starting location
            if random.random() < 0.3 and npc_templates:
                npc = random.choice(npc_templates)
                loc.npcs[npc.name.lower()] = npc
        
        # Set starting location
        self.map.set_current_location(list(self.map.locations.keys())[0])
        self.map.get_current_location().visited = True
    
    def _add_starting_items(self, genre: str):
        """Add starting items based on genre."""
        starting_items = [
            Item("Backpack", "A sturdy bag for carrying items", ItemType.QUEST),
            Item("Map", "A map of the land", ItemType.QUEST),
        ]
        
        # Add a weapon
        weapons = ItemFactory.get_weapons(genre)
        if weapons:
            starting_items.append(weapons[0])
        
        # Add a healing item
        healing = ItemFactory.get_healing_items()
        if healing:
            starting_items.append(healing[0])
        
        self.player.inventory.extend(starting_items)
    
    def process_command(self, command: str) -> str:
        """Process a player command."""
        self.turn_count += 1
        command = command.strip().lower()
        
        if not command:
            return "Please enter a command."
        
        parts = command.split(maxsplit=1)
        action = parts[0]
        target = parts[1] if len(parts) > 1 else ""
        
        handlers = {
            "look": self.cmd_look,
            "go": self.cmd_go,
            "north": lambda _: self.cmd_go("north"),
            "south": lambda _: self.cmd_go("south"),
            "east": lambda _: self.cmd_go("east"),
            "west": lambda _: self.cmd_go("west"),
            "take": self.cmd_take,
            "drop": self.cmd_drop,
            "inventory": self.cmd_inventory,
            "use": self.cmd_use,
            "equip": self.cmd_equip,
            "unequip": self.cmd_unequip,
            "talk": self.cmd_talk,
            "inspect": self.cmd_inspect,
            "status": self.cmd_status,
            "story": self.cmd_story,
            "attack": self.cmd_attack if self.state == GameState.IN_COMBAT else lambda _: "You're not in combat.",
            "defend": self.cmd_defend if self.state == GameState.IN_COMBAT else lambda _: "You're not in combat.",
            "heal": self.cmd_heal if self.state == GameState.IN_COMBAT else lambda _: "You're not in combat.",
            "flee": self.cmd_flee if self.state == GameState.IN_COMBAT else lambda _: "You're not in combat.",
            "help": self.cmd_help,
        }
        
        handler = handlers.get(action, lambda _: "Unknown command. Type 'help' for commands.")
        return handler(target)
    
    def cmd_look(self, target: str = "") -> str:
        """Look around or at something."""
        loc = self.map.get_current_location()
        if not loc:
            return "You're nowhere."
        
        response = f"\n�� {loc.name}\n"
        response += loc.descriptions.detailed + "\n"
        
        # Show exits
        if loc.transitions:
            response += "\nExits: " + ", ".join(loc.transitions.keys()) + "\n"
        
        # Show items
        if loc.items_on_ground:
            response += "\nItems here:\n"
            for item in loc.items_on_ground:
                response += f"  - {item.name}\n"
        
        # Show NPCs
        if loc.npcs:
            response += "\nPeople here:\n"
            for npc_name in loc.npcs:
                response += f"  - {npc_name}\n"
        
        return response
    
    def cmd_go(self, direction: str) -> str:
        """Move in a direction."""
        if not direction:
            return "Go where?"
        
        success, message = self.map.move(direction)
        if not success:
            return message
        
        # Entering new location
        loc = self.map.get_current_location()
        if loc and loc.visited:
            response = f"You're back at {loc.name}."
        else:
            response = loc.descriptions.first_time if loc else "You arrive somewhere."
        
        # Random encounter
        if self.encounters_enabled and random.random() < 0.3:
            response += "\n\n⚠️ An enemy appears!\n"
            self.start_encounter()
        
        return response
    
    def cmd_take(self, target: str) -> str:
        """Take an item."""
        if not target:
            return "Take what?"
        
        loc = self.map.get_current_location()
        if not loc or not loc.items_on_ground:
            return "There's nothing to take here."
        
        for item in loc.items_on_ground:
            if item.name.lower() == target.lower():
                self.player.inventory.append(item)
                loc.items_on_ground.remove(item)
                return f"You took the {item.name}."
        
        return f"There's no {target} here."
    
    def cmd_drop(self, target: str) -> str:
        """Drop an item."""
        if not target:
            return "Drop what?"
        
        for item in self.player.inventory:
            if item.name.lower() == target.lower():
                self.player.inventory.remove(item)
                loc = self.map.get_current_location()
                if loc:
                    loc.items_on_ground.append(item)
                return f"You dropped the {item.name}."
        
        return f"You don't have a {target}."
    
    def cmd_inventory(self, target: str = "") -> str:
        """Show inventory."""
        if not self.player.inventory:
            return "Your inventory is empty."
        
        response = "🎒 Inventory:\n"
        for item in self.player.inventory:
            response += f"  - {item.name}: {item.description}\n"
        
        if self.player.equipment_weapon:
            response += f"\n⚔️ Equipped Weapon: {self.player.equipment_weapon.name}\n"
        if self.player.equipment_armor:
            response += f"🛡️ Equipped Armor: {self.player.equipment_armor.name}\n"
        
        return response
    
    def cmd_use(self, target: str) -> str:
        """Use an item."""
        if not target:
            return "Use what?"
        
        for item in self.player.inventory:
            if item.name.lower() == target.lower():
                if item.item_type == ItemType.HEALING:
                    self.player.health = min(self.player.max_health, self.player.health + item.healing_amount)
                    if item.is_consumable:
                        self.player.inventory.remove(item)
                    return f"You used {item.name}. Restored {item.healing_amount} HP."
                return f"You can't use the {item.name} right now."
        
        return f"You don't have a {target}."
    
    def cmd_equip(self, target: str) -> str:
        """Equip a weapon or armor."""
        if not target:
            return "Equip what?"
        
        for item in self.player.inventory:
            if item.name.lower() == target.lower():
                if item.item_type == ItemType.WEAPON:
                    self.player.equipment_weapon = item
                    return f"You equipped {item.name}."
                elif item.item_type == ItemType.ARMOR:
                    self.player.equipment_armor = item
                    return f"You equipped {item.name}."
                return f"You can't equip the {item.name}."
        
        return f"You don't have a {target}."
    
    def cmd_unequip(self, target: str) -> str:
        """Unequip an item."""
        if not target:
            return "Unequip what?"
        
        if self.player.equipment_weapon and self.player.equipment_weapon.name.lower() == target.lower():
            self.player.equipment_weapon = None
            return f"You unequipped {target}."
        
        if self.player.equipment_armor and self.player.equipment_armor.name.lower() == target.lower():
            self.player.equipment_armor = None
            return f"You unequipped {target}."
        
        return f"You don't have that equipped."
    
    def cmd_talk(self, target: str) -> str:
        """Talk to an NPC."""
        if not target:
            return "Talk to whom?"
        
        loc = self.map.get_current_location()
        if not loc or target not in loc.npcs:
            return f"There's no {target} here."
        
        # Placeholder NPC interaction
        return f"The {target} says: 'Greetings, {self.player.name}. I'm here to help.'"
    
    def cmd_inspect(self, target: str) -> str:
        """Inspect an object in the location."""
        if not target:
            return "Inspect what?"
        
        return f"You examine the {target} carefully. Nothing special."
    
    def cmd_status(self, target: str = "") -> str:
        """Show player status."""
        damage = self.player.get_total_damage_bonus()
        armor = self.player.get_total_armor()
        
        response = f"""
Status:
  Name: {self.player.name}
  Health: {self.player.health}/{self.player.max_health}
  Damage Bonus: +{damage}
  Armor: {armor}
  Turns: {self.turn_count}
  Location: {self.map.get_current_location().name if self.map.get_current_location() else "Unknown"}
"""
        return response
    
    def cmd_story(self, target: str = "") -> str:
        """Show story progress."""
        if not self.story:
            return "No story loaded."
        
        return f"""
Story: {self.story.title}
Goal: {self.story.protagonist_goal}
Keywords: {', '.join(self.story.keywords)}
Current Progress: {self.current_story_node}
"""
    
    def cmd_attack(self, target: str = "") -> str:
        """Attack in combat."""
        if not self.combat_system or not self.combat_system.is_active:
            return "You're not in combat."
        
        damage = 5 + self.player.get_total_damage_bonus()
        result = self.combat_system.execute_action(CombatAction.ATTACK, str(damage))
        
        if result.get("victory"):
            # Check if this was a boss enemy
            is_boss = self.combat_system.enemy and self.combat_system.enemy.max_health > 50
            
            if is_boss:
                # Boss defeated = Story victory!
                response = result.get("message", "Victory!")
                response += f"\n\n🎉 YOU HAVE DEFEATED THE {self.combat_system.enemy.name.upper()}!\n"
                response += f"The curse is lifted and peace returns to the land!"
                self.state = GameState.VICTORY
                self.combat_system = None
                return response
            else:
                # Regular enemy defeated
                response = result.get("message", "Victory!")
                response += f"\n\nYou gain {random.randint(10, 50)} experience points!"
                self.state = GameState.EXPLORING
                self.combat_system = None
                return response
        
        if result.get("defeat"):
            self.state = GameState.DEFEAT
            return result.get("message", "You were defeated.")
        
        return result.get("message", "")
    
    def cmd_defend(self, target: str = "") -> str:
        """Defend in combat."""
        if not self.combat_system or not self.combat_system.is_active:
            return "You're not in combat."
        
        result = self.combat_system.execute_action(CombatAction.DEFEND)
        
        if result.get("victory"):
            is_boss = self.combat_system.enemy and self.combat_system.enemy.max_health > 50
            response = result.get("message", "Victory!")
            
            if is_boss:
                response += f"\n\n🎉 YOU HAVE DEFEATED THE {self.combat_system.enemy.name.upper()}!\n"
                response += f"The curse is lifted and peace returns to the land!"
                self.state = GameState.VICTORY
            else:
                response += f"\n\nYou gain {random.randint(10, 50)} experience points!"
                self.state = GameState.EXPLORING
            
            self.combat_system = None
            return response
        
        if result.get("defeat"):
            self.state = GameState.DEFEAT
            self.combat_system = None
            return result.get("message", "You were defeated.")
        
        return result.get("message", "")
    
    def cmd_heal(self, target: str = "") -> str:
        """Heal in combat."""
        if not self.combat_system or not self.combat_system.is_active:
            return "You're not in combat."
        
        healing_items = [item for item in self.player.inventory if item.item_type == ItemType.HEALING]
        if not healing_items:
            return "You have no healing items."
        
        item = healing_items[0]
        result = self.combat_system.execute_action(CombatAction.HEAL, str(item.healing_amount))
        
        if item.is_consumable:
            self.player.inventory.remove(item)
        
        if result.get("victory"):
            is_boss = self.combat_system.enemy and self.combat_system.enemy.max_health > 50
            response = result.get("message", "Victory!")
            
            if is_boss:
                response += f"\n\n🎉 YOU HAVE DEFEATED THE {self.combat_system.enemy.name.upper()}!\n"
                response += f"The curse is lifted and peace returns to the land!"
                self.state = GameState.VICTORY
            else:
                response += f"\n\nYou gain {random.randint(10, 50)} experience points!"
                self.state = GameState.EXPLORING
            
            self.combat_system = None
            return response
        
        if result.get("defeat"):
            self.state = GameState.DEFEAT
            self.combat_system = None
            return result.get("message", "You were defeated.")
        
        return result.get("message", "")
    
    def cmd_flee(self, target: str = "") -> str:
        """Try to flee from combat."""
        if not self.combat_system or not self.combat_system.is_active:
            return "You're not in combat."
        
        result = self.combat_system.execute_action(CombatAction.FLEE)
        
        if result.get("fled"):
            self.state = GameState.EXPLORING
            self.combat_system = None
        
        if result.get("defeat"):
            self.state = GameState.DEFEAT
            self.combat_system = None
        
        return result.get("message", "")
    
    def cmd_help(self, target: str = "") -> str:
        """Show help."""
        return """Available commands:
  look - Look around
  go <direction> - Move (north/south/east/west)
  take <item> - Take an item
  drop <item> - Drop an item
  inventory - Show inventory
  equip <item> - Equip weapon/armor
  unequip <item> - Remove equipment
  use <item> - Use an item
  talk <npc> - Talk to NPC
  inspect <object> - Inspect something
  status - Show status
  story - Show story progress
  attack - Attack in combat
  defend - Defend in combat
  heal - Heal in combat
  flee - Try to escape
  help - This message"""
    
    def start_encounter(self):
        """Start a combat encounter."""
        self.state = GameState.IN_COMBAT
        
        # Decide if this should be a boss encounter
        is_boss = self.turn_count > 40 and random.random() < 0.3
        
        if is_boss:
            # Boss encounter
            antagonist = self.story.protagonist_goal.split("Stop ")[1].split(" ")[0] if "Stop " in self.story.protagonist_goal else "Dark Lord"
            enemy = Enemy(
                name=antagonist,
                health=80,
                max_health=80,
                damage=15,
                armor=5,
            )
            message = f"\n⚠️  BOSS ENCOUNTER! {antagonist} appears!\n"
        else:
            # Regular encounter
            enemy_names = ["Goblin", "Orc", "Skeleton", "Shadow", "Bandit", "Minion"]
            enemy_name = random.choice(enemy_names)
            
            enemy = Enemy(
                name=enemy_name,
                health=30,
                max_health=30,
                damage=8,
                armor=2,
            )
            message = ""
        
        self.combat_system = CombatSystem(self.player.health, self.player.get_total_armor())
        self.combat_system.start_encounter(enemy)
        
        if message:
            print(message)
    
    def is_running(self) -> bool:
        """Check if game is running."""
        return self.state == GameState.EXPLORING or self.state == GameState.IN_COMBAT
