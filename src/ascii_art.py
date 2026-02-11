"""ASCII art and visual elements for the adventure game."""

import random

# Welcome banner
WELCOME_BANNER = r"""
    ___    ____  _    ___             __                    
   / _ |  / __ \/ |  / (_)  ______  / /_  ____  ________   
  / __ | / /_/ /| | / / /  / ___/ / __ \/ __ \/ ___/ __ \  
 / ___ |/ _, _/ | |/ / /  (__  ) / /_/ / /_/ / /  / /_/ /  
/_/  |_/_/ |_|  |___/_/  /____/  /_.___/\____/_/   \____/   

         Welcome to the CLI Adventure!
      Each journey is unique and endless...
"""

SWORD = """
    /\\
   /  \\
  /    \\
 /______\\
    ||
    ||
"""

DRAGON = """
    /^\\___
   /  > ___)
  /   |_/
 /    |\\
/     | \\
\\    /   \\
 \\  /     \\
  \\/       \\
"""

TREASURE = """
  ___________
 |___________|
 |* *  * * * |
 |___________|
  |||||||||
"""

FOREST = """
    \\|/
   --*--
    /|\\
   / | \\
  /  |  \\
     |
    \\|/
   --*--
    /|\\
"""

CAVE = """
     ___
   /~   ~\\
  /       \\
 |  /|||\\  |
 | / ||| \\ |
 |     O   |
  \\       /
   \\_   _/
     ~|~
"""

CREATURE_ENCOUNTERS = {
    "goblin": """
       (o_o)
      /|___|\\ 
       / | \\
      /  |  \\
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
    "witch": """
        _
       | |
      /| |\\
     / | | \\
       | |
      /   \\
""",
}

def get_random_ascii_art():
    """Return a random ASCII art piece for flavor."""
    arts = [FOREST, CAVE, SWORD, TREASURE]
    return random.choice(arts)

def get_creature_art(creature_name):
    """Get ASCII art for a specific creature."""
    return CREATURE_ENCOUNTERS.get(creature_name, "")

def print_banner(text):
    """Print a formatted banner."""
    width = 60
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width + "\n")

def print_scene_divider():
    """Print a scene divider."""
    print("\n" + "-" * 60 + "\n")
