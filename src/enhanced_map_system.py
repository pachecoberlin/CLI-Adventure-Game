"""Enhanced map system with proper graph-based navigation."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ConnectionType(Enum):
    """Types of connections between locations."""
    NORMAL = "normal"  # Bidirectional path
    ONE_WAY = "one_way"  # Can't go back
    LOCKED = "locked"  # Requires item to unlock
    TELEPORT = "teleport"  # Magic transportation
    SPECIAL = "special"  # Requires action/story step
    ENTER = "enter"  # Enter a building/location
    EXIT = "exit"  # Leave a building


@dataclass
class Connection:
    """A connection between two locations."""
    from_loc: str
    to_loc: str
    direction: str  # "north", "south", "enter tavern", etc
    type: ConnectionType = ConnectionType.NORMAL
    description: str = "You travel..."
    locked_by_item: Optional[str] = None
    locked_by_step: Optional[str] = None
    is_bidirectional: bool = True
    return_direction: Optional[str] = None


@dataclass
class GameObject:
    """An object in a location that can contain items."""
    id: str
    name: str
    description: str
    is_container: bool = False
    can_open: bool = False
    is_locked: bool = False
    locked_by_item: Optional[str] = None
    items: List[str] = field(default_factory=list)  # Item IDs
    is_inspectable: bool = True


@dataclass  
class Location:
    """A location in the game world."""
    id: str
    name: str
    short_description: str  # "You are back at..."
    first_visit_description: str  # Detailed first time
    detailed_description: str  # `look` command
    
    connections: Dict[str, str] = field(default_factory=dict)  # direction -> to_loc_id
    objects: Dict[str, GameObject] = field(default_factory=dict)  # object_id -> object
    
    visited: bool = False
    is_locked: bool = False
    locked_by_item: Optional[str] = None
    locked_by_step: Optional[str] = None
    
    atmosphere: str = "Neutral"
    npcs_present: List[str] = field(default_factory=list)
    story_relevant: bool = False


class EnhancedMap:
    """Enhanced map with proper graph-based navigation."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.connections: List[Connection] = []
        self.current_location_id: Optional[str] = None
    
    def add_location(self, location: Location):
        """Add a location to the map."""
        self.locations[location.id] = location
    
    def add_connection(self, connection: Connection):
        """Add a connection between locations."""
        self.connections.append(connection)
        
        # Add forward direction
        if connection.to_loc not in self.locations[connection.from_loc].connections.values():
            self.locations[connection.from_loc].connections[connection.direction] = connection.to_loc
        
        # Add return direction if bidirectional
        if connection.is_bidirectional and connection.from_loc not in self.locations[connection.to_loc].connections.values():
            return_dir = connection.return_direction or self._opposite_direction(connection.direction)
            self.locations[connection.to_loc].connections[return_dir] = connection.from_loc
    
    def get_current_location(self) -> Optional[Location]:
        """Get the current location."""
        return self.locations.get(self.current_location_id)
    
    def set_current_location(self, location_id: str):
        """Set the current location."""
        if location_id in self.locations:
            self.current_location_id = location_id
            if not self.locations[location_id].visited:
                self.locations[location_id].visited = True
    
    def can_move(self, direction: str) -> Tuple[bool, str]:
        """Check if player can move in a direction."""
        loc = self.get_current_location()
        if not loc:
            return False, "You are nowhere."
        
        if direction not in loc.connections:
            return False, f"You can't go {direction} from here."
        
        to_loc_id = loc.connections[direction]
        to_loc = self.locations[to_loc_id]
        
        # Check if locked
        if to_loc.is_locked:
            if to_loc.locked_by_item:
                return False, f"The path is blocked. You need {to_loc.locked_by_item}."
            if to_loc.locked_by_step:
                return False, "You are not ready to go there yet."
        
        return True, ""
    
    def move(self, direction: str) -> Tuple[bool, str]:
        """Try to move in a direction."""
        can_move, reason = self.can_move(direction)
        
        if not can_move:
            return False, reason
        
        to_loc_id = self.get_current_location().connections[direction]
        self.set_current_location(to_loc_id)
        
        loc = self.get_current_location()
        if loc.visited:
            return True, f"You are back at {loc.name}."
        else:
            return True, loc.first_visit_description
    
    def get_available_directions(self) -> List[str]:
        """Get available directions from current location."""
        loc = self.get_current_location()
        if not loc:
            return []
        
        available = []
        for direction, to_loc_id in loc.connections.items():
            to_loc = self.locations[to_loc_id]
            # Check if locked
            if not to_loc.is_locked:
                available.append(direction)
        
        return available
    
    @staticmethod
    def _opposite_direction(direction: str) -> str:
        """Get opposite direction."""
        opposites = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
            "up": "down",
            "down": "up",
        }
        return opposites.get(direction.lower(), "back")
