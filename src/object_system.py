"""Object and container system for item discovery."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class GameObject:
    """An object/container in a location."""
    id: str
    name: str  # "chest", "painting", "statue", "drawer"
    display_name: str  # "an old wooden chest"
    description: str  # Full description
    
    # Container properties
    is_container: bool = False
    can_open: bool = True
    is_open: bool = False
    is_locked: bool = False
    
    # What's inside
    items: List[str] = field(default_factory=list)  # Item names/ids
    hidden_hint: str = ""  # Hint about what's inside
    
    # Requirements
    requires_item: Optional[str] = None  # Item needed to open/unlock
    requires_action: Optional[str] = None  # Action needed (e.g., "solve riddle")
    
    # Discovery
    is_obvious: bool = True  # Is object visible without searching?
    can_examine: bool = True
    can_search: bool = True


class ObjectSystem:
    """Manages objects and containers in locations."""
    
    # Standard object templates
    CONTAINER_TEMPLATES = {
        "fantasy": [
            {
                "name": "wooden chest",
                "description": "A large wooden chest with brass hinges, covered in dust.",
                "is_container": True,
                "can_open": True,
            },
            {
                "name": "stone altar",
                "description": "An ancient stone altar with mysterious carvings.",
                "is_container": True,
                "can_open": False,
                "is_obvious": False,
            },
            {
                "name": "bookshelf",
                "description": "Towering shelves filled with ancient tomes.",
                "can_examine": True,
                "can_search": True,
            },
            {
                "name": "sword rack",
                "description": "An ornate rack displaying weapons.",
                "is_obvious": True,
            },
        ],
        "scifi": [
            {
                "name": "storage locker",
                "description": "A sealed metal storage locker with a keypad.",
                "is_container": True,
                "is_locked": True,
                "requires_item": "access_card",
            },
            {
                "name": "server console",
                "description": "A blinking computer terminal with screens.",
                "can_examine": True,
            },
            {
                "name": "weapons cache",
                "description": "A hidden weapons storage compartment.",
                "is_container": True,
                "is_obvious": False,
            },
        ],
        "detective": [
            {
                "name": "filing cabinet",
                "description": "Old metal drawers with case files.",
                "is_container": True,
            },
            {
                "name": "safe",
                "description": "A heavy wall safe with a combination lock.",
                "is_container": True,
                "is_locked": True,
                "requires_action": "crack_combination",
            },
            {
                "name": "desk",
                "description": "A cluttered desk with scattered papers.",
                "can_search": True,
            },
        ],
        "horror": [
            {
                "name": "coffin",
                "description": "An ancient stone coffin with carved runes.",
                "is_container": True,
                "is_obvious": False,
            },
            {
                "name": "crypt door",
                "description": "A sealed metal door to the crypt.",
                "is_container": True,
                "is_locked": True,
                "requires_item": "key",
            },
        ],
    }
    
    @staticmethod
    def create_object(
        obj_id: str,
        name: str,
        description: str,
        is_container: bool = False,
        items: List[str] = None,
        **kwargs
    ) -> GameObject:
        """Create a game object."""
        return GameObject(
            id=obj_id,
            name=name,
            display_name=f"a {name}",
            description=description,
            is_container=is_container,
            items=items or [],
            **kwargs
        )
    
    @staticmethod
    def open_container(obj: GameObject, player_items: List[str] = None) -> Tuple[bool, str]:
        """Try to open a container."""
        if not obj.is_container:
            return False, f"The {obj.name} can't be opened."
        
        if obj.is_open:
            return True, f"The {obj.name} is already open."
        
        if not obj.can_open:
            return False, f"The {obj.name} cannot be opened."
        
        if obj.is_locked:
            if obj.requires_item:
                if player_items and obj.requires_item in player_items:
                    obj.is_locked = False
                    obj.is_open = True
                    return True, f"You use the {obj.requires_item} to open the {obj.name}."
                else:
                    return False, f"The {obj.name} is locked. You need {obj.requires_item}."
            else:
                return False, f"The {obj.name} is locked."
        
        obj.is_open = True
        if obj.items:
            return True, f"You open the {obj.name} and find: {', '.join(obj.items)}"
        else:
            return True, f"You open the {obj.name}. It's empty."
    
    @staticmethod
    def examine_object(obj: GameObject) -> str:
        """Examine an object."""
        if not obj.can_examine:
            return f"There's nothing special about the {obj.name}."
        
        text = obj.description
        
        if obj.is_container and obj.is_open and obj.items:
            text += f"\nInside you see: {', '.join(obj.items)}"
        elif obj.is_obvious is False:
            text += "\nThis location holds secrets..."
        
        return text
    
    @staticmethod
    def search_location(objects: Dict[str, GameObject]) -> str:
        """Search a location for hidden objects."""
        found = []
        for obj in objects.values():
            if not obj.is_obvious:
                found.append(obj)
        
        if found:
            return f"You discover: {', '.join([o.name for o in found])}"
        else:
            return "You don't find anything hidden here."
