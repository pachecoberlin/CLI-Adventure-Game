"""AI-powered story generator for dynamic adventures."""

import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class StoryNode:
    """Represents a step in the story."""
    id: str
    title: str
    description: str
    objectives: List[str] = field(default_factory=list)
    rewards: List[str] = field(default_factory=list)
    next_nodes: Dict[str, str] = field(default_factory=dict)  # condition -> node_id


@dataclass
class Story:
    """A complete story with locations and progression."""
    title: str
    theme: str
    protagonist_goal: str
    locations: List[str]
    nodes: Dict[str, StoryNode]
    start_node: str
    end_node: str
    keywords: List[str]


class StoryGenerator:
    """Generates stories using templates and AI."""
    
    STORY_TEMPLATES = {
        "fantasy": {
            "themes": ["rescue", "revenge", "treasure_hunt", "escape"],
            "antagonists": ["Dark Lord", "Evil Sorcerer", "Dragon", "Cursed King"],
            "rewards": ["Ancient Crown", "Magic Artifact", "Lost Kingdom", "Redemption"],
            "locations_count": 5,
        },
        "scifi": {
            "themes": ["escape_planet", "repair_ship", "stop_invasion", "retrieve_data"],
            "antagonists": ["AI Overlord", "Alien Hive", "Rogue AI", "Corporate Enemy"],
            "rewards": ["Freedom", "Power Source", "Cure", "Truth"],
            "locations_count": 5,
        },
        "detective": {
            "themes": ["solve_murder", "find_culprit", "uncover_conspiracy", "recover_artifact"],
            "antagonists": ["Serial Killer", "Crime Boss", "Corrupt Official", "Mastermind"],
            "rewards": ["Justice", "Truth", "Redemption", "Solved Case"],
            "locations_count": 5,
        },
        "horror": {
            "themes": ["survive_night", "break_curse", "escape_evil", "save_town"],
            "antagonists": ["Ancient Evil", "Possessed Spirit", "Creature", "Cult Leader"],
            "rewards": ["Safety", "Peace", "Redemption", "Knowledge"],
            "locations_count": 5,
        },
    }
    
    @classmethod
    def generate_story(cls, genre: str, keywords: List[str], player_name: str) -> Story:
        """Generate a complete story from genre and keywords."""
        
        template = cls.STORY_TEMPLATES.get(genre.lower(), cls.STORY_TEMPLATES["fantasy"])
        
        theme = random.choice(template["themes"])
        antagonist = random.choice(template["antagonists"])
        reward = random.choice(template["rewards"])
        
        # Create base story
        title = f"The {theme.replace('_', ' ').title()} of {antagonist}"
        protagonist_goal = f"Stop {antagonist} and claim the {reward}"
        
        # Generate story nodes
        nodes = cls._generate_story_nodes(theme, antagonist, reward, player_name)
        
        # Generate locations
        locations = cls._generate_locations(genre, keywords, template["locations_count"])
        
        story = Story(
            title=title,
            theme=theme,
            protagonist_goal=protagonist_goal,
            locations=locations,
            nodes=nodes,
            start_node="start",
            end_node="victory",
            keywords=keywords,
        )
        
        return story
    
    @classmethod
    def _generate_story_nodes(cls, theme: str, antagonist: str, reward: str, player_name: str) -> Dict[str, StoryNode]:
        """Generate story progression nodes."""
        
        nodes = {
            "start": StoryNode(
                id="start",
                title="The Beginning",
                description=f"You are {player_name}, and you've heard rumors about {antagonist}.",
                objectives=[f"Find information about {antagonist}", "Prepare for the journey"],
                next_nodes={"explore": "investigation"}
            ),
            "investigation": StoryNode(
                id="investigation",
                title="Investigation",
                description=f"You must gather clues and find allies to defeat {antagonist}.",
                objectives=["Find three clues", "Meet at least one ally"],
                next_nodes={"clues_found": "confrontation"}
            ),
            "confrontation": StoryNode(
                id="confrontation",
                title="Face Off",
                description=f"It's time to confront {antagonist} and claim the {reward}.",
                objectives=[f"Defeat {antagonist}", f"Claim the {reward}"],
                next_nodes={"victory_earned": "victory"}
            ),
            "victory": StoryNode(
                id="victory",
                title="Victory",
                description=f"You have defeated {antagonist} and obtained the {reward}. Your journey is complete.",
                objectives=[],
                next_nodes={}
            ),
        }
        
        return nodes
    
    @classmethod
    def _generate_locations(cls, genre: str, keywords: List[str], count: int) -> List[str]:
        """Generate location names based on genre and keywords."""
        
        location_templates = {
            "fantasy": ["Dark Forest", "Ancient Temple", "Mountain Peak", "Cursed Village", "Dragon's Lair"],
            "scifi": ["Space Station", "Alien World", "Research Lab", "Crashed Ship", "Dystopian City"],
            "detective": ["Crime Scene", "Police Station", "Abandoned Building", "Underground Hideout", "City Street"],
            "horror": ["Haunted Mansion", "Abandoned Hospital", "Dark Graveyard", "Cursed Church", "Witch's Cottage"],
        }
        
        locations = location_templates.get(genre.lower(), location_templates["fantasy"])[:count]
        return locations
    
    @classmethod
    def story_to_dict(cls, story: Story) -> Dict:
        """Convert story to dict for serialization."""
        return {
            "title": story.title,
            "theme": story.theme,
            "protagonist_goal": story.protagonist_goal,
            "locations": story.locations,
            "keywords": story.keywords,
        }
