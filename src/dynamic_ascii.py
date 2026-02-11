"""Dynamic ASCII art generation based on context."""

import random


class DynamicASCII:
    """Generate ASCII art dynamically for locations, items, NPCs."""
    
    LOCATION_ART = {
        "forest": [
            """
    \\|/
   --*--
    /|\\
   / | \\
  /  |  \\
     |
    \\|/
   --*--
    /|\\
            """,
        ],
        "castle": [
            """
      |\\
      | \\
    \\-+-/
     |=|
    /| |\\
   / | | \\
  |  | |  |
            """,
        ],
        "cave": [
            """
     ___
   /~   ~\\
  /       \\
 |  /|||\\  |
 | / ||| \\ |
 |     O   |
  \\       /
   \\_   _/
      ~|~
            """,
        ],
        "city": [
            """
  ___   ___
 |___|_|___|
 |_|_____||_|
 |__|_|___|_|
  _|_______|
 |_|_____|_|
            """,
        ],
        "spaceship": [
            """
    \\     /
     \\___/
    _|___|_
   |_______|
   |  |||  |
   |_|||||_|
     /||||\\
    /_||||_\\
            """,
        ],
    }
    
    ITEM_ART = {
        "sword": """
    /\\
   /  \\
  /    \\
 /______\\
    ||
    ||
        """,
        "shield": """
   /-----\\
  |   O   |
  |       |
   \\     /
    \\   /
     \\_/
        """,
        "potion": """
   _____
  /     \\
 | () () |
 |   V   |
  \\_____/
    |||
        """,
        "key": """
   o--O--,
  /      \\
 |        |
  \\_____/
        """,
    }
    
    CREATURE_ART = {
        "goblin": """
       (o_o)
      /|___|\\
       / | \\
      /  |  \\
        """,
        "dragon": """
    /^\\___
   /  > ___)
  /   |_/
 /    |\\
/     | \\
        """,
        "skeleton": """
        ___
       |___|
      /|   |\\
       | O |
      /|___|\\
        | |
       /   \\
        """,
        "ghost": """
     /~~~~~\\
    |  o o  |
    |   >   |
     \\  V  /
      |___|
     _||_||_
    / || || \\
        """,
    }
    
    @classmethod
    def get_location_art(cls, location_type: str) -> str:
        """Get ASCII art for a location."""
        options = cls.LOCATION_ART.get(location_type.lower(), [])
        if options:
            return random.choice(options)
        return ""
    
    @classmethod
    def get_item_art(cls, item_name: str) -> str:
        """Get ASCII art for an item."""
        return cls.ITEM_ART.get(item_name.lower(), "")
    
    @classmethod
    def get_creature_art(cls, creature_name: str) -> str:
        """Get ASCII art for a creature."""
        return cls.CREATURE_ART.get(creature_name.lower(), "")
    
    @classmethod
    def get_random_art(cls) -> str:
        """Get random ASCII art."""
        all_art = (
            list(cls.LOCATION_ART.values()) +
            list(cls.ITEM_ART.values()) +
            list(cls.CREATURE_ART.values())
        )
        flat_art = [art for sublist in all_art for art in (sublist if isinstance(sublist, list) else [sublist])]
        return random.choice(flat_art) if flat_art else ""
