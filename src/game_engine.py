"""Core game engine for the CLI adventure."""

import random
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum


class GameState(Enum):
    """Enum for game states."""
    STARTING = "starting"
    EXPLORING = "exploring"
    IN_COMBAT = "in_combat"
    VICTORY = "victory"
    DEFEAT = "defeat"
    QUIT = "quit"


@dataclass
class Item:
    """Represents an item in the game."""
    name: str
    description: str
    usable: bool = False


@dataclass
class Character:
    """Represents a game character."""
    name: str
    health: int = 100
    inventory: List[Item] = field(default_factory=list)
    
    def take_item(self, item: Item) -> bool:
        """Add item to inventory."""
        if len(self.inventory) < 10:
            self.inventory.append(item)
            return True
        return False
    
    def drop_item(self, item_name: str) -> Optional[Item]:
        """Remove item from inventory."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                return item
        return None
    
    def has_item(self, item_name: str) -> bool:
        """Check if character has an item."""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def get_item(self, item_name: str) -> Optional[Item]:
        """Get an item by name."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def take_damage(self, amount: int):
        """Reduce health."""
        self.health = max(0, self.health - amount)
    
    def heal(self, amount: int):
        """Increase health."""
        self.health = min(100, self.health + amount)
    
    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.health > 0


@dataclass
class Location:
    """Represents a location in the game world."""
    name: str
    description: str
    exits: Dict[str, 'Location'] = field(default_factory=dict)
    items: List[Item] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)


class Adventure:
    """Main game engine."""
    
    def __init__(self, interest: str, player_name: str = "Adventurer"):
        self.interest = interest
        self.player = Character(name=player_name)
        self.current_location: Optional[Location] = None
        self.state = GameState.STARTING
        self.turn_count = 0
        self.visited_locations: set = set()
        self.completed_objectives: set = set()
        self.history: List[str] = []
        
    def start_game(self):
        """Initialize the game."""
        self.state = GameState.EXPLORING
        self.turn_count = 0
        self._setup_world()
    
    def _setup_world(self):
        """Create the game world based on interest."""
        # Create starting location
        start_desc = f"You find yourself in a mysterious realm tailored to {self.interest}..."
        start_loc = Location("Starting Point", start_desc)
        
        # Add some basic items
        start_loc.items.append(Item("torch", "A flickering torch that provides light", usable=True))
        
        self.current_location = start_loc
        self.visited_locations.add("Starting Point")
    
    def process_command(self, command: str) -> str:
        """Process player command."""
        self.turn_count += 1
        command = command.strip().lower()
        
        if not command:
            return "Please enter a valid command."
        
        # Parse command
        parts = command.split(maxsplit=1)
        action = parts[0]
        target = parts[1] if len(parts) > 1 else ""
        
        # Command handlers
        handlers = {
            "look": self.cmd_look,
            "go": self.cmd_go,
            "take": self.cmd_take,
            "drop": self.cmd_drop,
            "inventory": self.cmd_inventory,
            "use": self.cmd_use,
            "help": self.cmd_help,
            "status": self.cmd_status,
        }
        
        handler = handlers.get(action, lambda x: "Unknown command. Type 'help' for available commands.")
        response = handler(target)
        self.history.append(f"> {command}\n{response}")
        return response
    
    def cmd_look(self, target: str = "") -> str:
        """Describe current location."""
        if not self.current_location:
            return "You are nowhere."
        
        response = f"\n📍 {self.current_location.name}\n"
        response += f"{self.current_location.description}\n"
        
        if self.current_location.items:
            response += "\nItems here:\n"
            for item in self.current_location.items:
                response += f"  - {item.name}\n"
        
        if self.current_location.exits:
            response += "\nYou can go:\n"
            for direction in self.current_location.exits:
                response += f"  - {direction}\n"
        
        return response
    
    def cmd_go(self, direction: str) -> str:
        """Move to a new location."""
        if not direction:
            return "Go where? Specify a direction."
        
        if not self.current_location or direction not in self.current_location.exits:
            return f"You can't go {direction} from here."
        
        self.current_location = self.current_location.exits[direction]
        self.visited_locations.add(self.current_location.name)
        return self.cmd_look()
    
    def cmd_take(self, target: str) -> str:
        """Pick up an item."""
        if not target:
            return "Take what?"
        
        if not self.current_location:
            return "You can't take anything here."
        
        for item in self.current_location.items:
            if item.name.lower() == target.lower():
                if self.player.take_item(item):
                    self.current_location.items.remove(item)
                    return f"You took the {item.name}."
                return "Your inventory is full!"
        
        return f"There is no {target} here."
    
    def cmd_drop(self, target: str) -> str:
        """Drop an item."""
        if not target:
            return "Drop what?"
        
        item = self.player.drop_item(target)
        if item and self.current_location:
            self.current_location.items.append(item)
            return f"You dropped the {item.name}."
        
        return f"You don't have a {target}."
    
    def cmd_inventory(self, target: str = "") -> str:
        """Show inventory."""
        if not self.player.inventory:
            return "Your inventory is empty."
        
        response = "Inventory:\n"
        for item in self.player.inventory:
            response += f"  - {item.name}: {item.description}\n"
        return response
    
    def cmd_use(self, target: str) -> str:
        """Use an item."""
        if not target:
            return "Use what?"
        
        item = self.player.get_item(target)
        if not item:
            return f"You don't have a {target}."
        
        if not item.usable:
            return f"You can't use the {item.name}."
        
        return f"You use the {item.name}. Something happens..."
    
    def cmd_help(self, target: str = "") -> str:
        """Show available commands."""
        return """Available commands:
  look - Describe your surroundings
  go <direction> - Move in a direction (north, south, east, west)
  take <item> - Pick up an item
  drop <item> - Drop an item from inventory
  inventory - Show your inventory
  use <item> - Use an item
  status - Check your health and stats
  help - Show this help message"""
    
    def cmd_status(self, target: str = "") -> str:
        """Show player status."""
        return f"""Status:
  Name: {self.player.name}
  Health: {self.player.health}/100
  Turns: {self.turn_count}
  Locations visited: {len(self.visited_locations)}"""
    
    def is_running(self) -> bool:
        """Check if game is still running."""
        return self.state == GameState.EXPLORING
