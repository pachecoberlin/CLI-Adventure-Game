"""Scenario generator that creates dynamic adventures."""

import random
from typing import List, Dict
from src.game_engine import Location, Item, Adventure


class ScenarioGenerator:
    """Generates adventure scenarios based on player interests."""
    
    SCENARIOS = {
        "fantasy": {
            "locations": [
                ("Enchanted Forest", "Ancient trees loom overhead, their twisted branches forming intricate patterns. The air smells of moss and magic."),
                ("Dragon's Lair", "A massive cavern filled with gold and precious gems. The air is hot and smells of sulfur."),
                ("Village Square", "A bustling medieval village with stone buildings and a central fountain."),
                ("Dark Castle", "An imposing stone castle with towering spires. Dark clouds swirl above its highest towers."),
                ("Mystical Lake", "A serene lake surrounded by willows. Strange lights flicker beneath the water's surface."),
            ],
            "items": [
                ("sword", "A gleaming steel sword with an ornate hilt"),
                ("shield", "A wooden shield reinforced with iron bands"),
                ("spell_book", "An ancient tome of arcane knowledge", True),
                ("potion", "A glowing elixir", True),
                ("amulet", "A protective charm"),
            ],
            "npcs": ["Wizard", "Elf", "Dwarf", "Merchant"],
        },
        "scifi": {
            "locations": [
                ("Space Station", "A sleek space station orbiting a distant planet. Holographic displays flicker with data."),
                ("Alien Planet", "A barren landscape with strange rock formations and two moons in the sky."),
                ("Cyberpunk City", "Neon signs and flying vehicles fill a bustling futuristic metropolis."),
                ("Underground Bunker", "A fortified bunker with steel walls and blinking control panels."),
                ("Abandoned Ship", "A derelict spacecraft drifting through space, its corridors dark and silent."),
            ],
            "items": [
                ("laser_gun", "A compact energy weapon"),
                ("scanner", "A handheld device for analyzing surroundings", True),
                ("data_disk", "Contains valuable information"),
                ("repair_kit", "For fixing broken technology", True),
                ("helmet", "A protective suit helmet"),
            ],
            "npcs": ["Robot", "Alien", "Cyborg", "Captain"],
        },
        "detective": {
            "locations": [
                ("Crime Scene", "Yellow tape marks the perimeter. Evidence markers dot the scene."),
                ("Police Station", "A bustling precinct filled with detectives working cases."),
                ("Suspect's House", "A modest home with signs of struggle. Drawers hang open."),
                ("Dark Alley", "A narrow passage between buildings, shrouded in shadows."),
                ("Bar", "A dimly lit establishment filled with shadowy figures."),
            ],
            "items": [
                ("magnifying_glass", "For examining evidence", True),
                ("notebook", "For taking notes", True),
                ("badge", "Your detective's badge"),
                ("revolver", "A loaded firearm"),
                ("clue", "A mysterious piece of evidence"),
            ],
            "npcs": ["Witness", "Suspect", "Informant", "Partner"],
        },
        "horror": {
            "locations": [
                ("Haunted Mansion", "A decrepit estate, its paint peeling and windows broken. Strange sounds echo from within."),
                ("Graveyard", "Tombstones litter a fog-covered field. The air is cold and damp."),
                ("Basement", "Dark and dank, with chains on the walls and an oppressive atmosphere."),
                ("Abandoned Hospital", "Flickering lights and the sound of dripping water. Medical equipment lies scattered."),
                ("Forest at Night", "Twisted trees and dense fog. Something moves just beyond your vision."),
            ],
            "items": [
                ("lantern", "Dispels the darkness", True),
                ("cross", "A holy symbol for protection"),
                ("garlic", "Said to ward off creatures"),
                ("salt", "A protective barrier", True),
                ("ancient_text", "Contains forbidden knowledge"),
            ],
            "npcs": ["Ghost", "Vampire", "Werewolf", "Curse"],
        },
    }
    
    @classmethod
    def generate_world(cls, adventure: Adventure) -> None:
        """Generate the game world based on interest."""
        interest = adventure.interest.lower()
        
        # Default to fantasy if interest not found
        scenario = cls.SCENARIOS.get(interest, cls.SCENARIOS["fantasy"])
        
        # Create locations
        locations_data = scenario["locations"]
        locations = {}
        
        for loc_name, loc_desc in locations_data:
            locations[loc_name] = Location(loc_name, loc_desc)
        
        # Connect locations randomly
        location_list = list(locations.values())
        for i, loc in enumerate(location_list):
            directions = ["north", "south", "east", "west"]
            random.shuffle(directions)
            
            for j, direction in enumerate(directions):
                if j < len(location_list) - 1:
                    next_loc = location_list[(i + j + 1) % len(location_list)]
                    loc.exits[direction] = next_loc
        
        # Add items to locations
        items_data = scenario["items"]
        items = [Item(name, desc, usable) for name, desc, *usable in items_data]
        
        for item in items:
            random.choice(location_list).items.append(item)
        
        # Add NPCs
        for loc in location_list:
            npcs = scenario["npcs"]
            if random.random() > 0.5:
                loc.npcs.append(random.choice(npcs))
        
        # Set starting location
        adventure.current_location = location_list[0]
        adventure.visited_locations.add(location_list[0].name)
    
    @classmethod
    def get_scenario_description(cls, interest: str) -> str:
        """Get a description of the scenario."""
        descriptions = {
            "fantasy": "You awaken in a world of magic and mystery...",
            "scifi": "You wake up in a distant future filled with advanced technology...",
            "detective": "You're on the case. Time to start investigating...",
            "horror": "Something feels very wrong. The darkness seems to watch you...",
        }
        return descriptions.get(interest.lower(), "Your adventure begins...")
