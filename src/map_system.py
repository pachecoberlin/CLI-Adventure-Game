"""Map system with fixed routes, dead ends, and special transitions."""

from typing import Dict, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class TransitionType(Enum):
    """Types of transitions between locations."""
    NORMAL = "normal"  # Regular direction-based exit
    ENTER = "enter"  # Enter a building/location
    TELEPORT = "teleport"  # Magical/tech teleportation
    ONE_WAY = "one_way"  # Can't go back
    SPECIAL = "special"  # Requires item or action


@dataclass
class Transition:
    """Represents a connection between locations."""
    destination: str
    transition_type: TransitionType = TransitionType.NORMAL
    requires_item: Optional[str] = None  # Item needed to traverse
    description: str = "You move to a new location."
    is_locked: bool = False
    lock_reason: str = ""


@dataclass
class LocationDescription:
    """Descriptions for a location at different times."""
    first_time: str  # Initial description when first entering
    revisit_short: str  # Short description when returning
    detailed: str  # Full description when using 'look'


@dataclass
class InspectableObject:
    """An object that can be inspected for details/items."""
    name: str
    description: str  # What you see when you inspect
    hidden_item: Optional[str] = None  # Item found by inspecting


@dataclass
class Location:
    """A location in the game world."""
    id: str
    name: str
    descriptions: LocationDescription
    transitions: Dict[str, Transition] = field(default_factory=dict)  # direction -> transition
    inspectable_objects: Dict[str, InspectableObject] = field(default_factory=dict)  # object_name -> object
    initial_visit: bool = True
    visited: bool = False
    npcs: Dict[str, 'NPC'] = field(default_factory=dict)  # NPC name -> NPC object
    items_on_ground: List['Item'] = field(default_factory=list)  # Items available


class Map:
    """The game world map with fixed routes."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_location_id: Optional[str] = None
    
    def add_location(self, location: Location):
        """Add a location to the map."""
        self.locations[location.id] = location
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID."""
        return self.locations.get(location_id)
    
    def get_current_location(self) -> Optional[Location]:
        """Get the current location."""
        if self.current_location_id:
            return self.get_location(self.current_location_id)
        return None
    
    def set_current_location(self, location_id: str) -> bool:
        """Move to a location."""
        if location_id in self.locations:
            self.current_location_id = location_id
            return True
        return False
    
    def move(self, direction: str) -> tuple[bool, str]:
        """
        Try to move in a direction.
        Returns (success, message)
        """
        current = self.get_current_location()
        if not current:
            return False, "You are nowhere."
        
        if direction not in current.transitions:
            return False, f"You can't go {direction} from here."
        
        transition = current.transitions[direction]
        
        if transition.is_locked:
            return False, f"You can't go that way. {transition.lock_reason}"
        
        # Move to destination
        self.set_current_location(transition.destination)
        dest = self.get_current_location()
        
        if dest:
            dest.visited = True
            return True, transition.description
        
        return False, "Something went wrong."
    
    def get_available_exits(self) -> Dict[str, str]:
        """Get all available exits from current location."""
        current = self.get_current_location()
        if not current:
            return {}
        
        exits = {}
        for direction, transition in current.transitions.items():
            if not transition.is_locked:
                exits[direction] = transition.destination
        
        return exits
