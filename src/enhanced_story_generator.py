"""Enhanced story generator with AI-powered narrative creation."""

import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class StoryStep:
    """A single step in the story progression."""
    id: str
    title: str
    description: str
    location_ids: List[str]  # Which locations this step occurs at
    required_item: Optional[str] = None  # Item needed to progress
    unlocks_location: Optional[str] = None  # Location unlocked by completing this
    is_optional: bool = False
    npc_involved: Optional[str] = None


@dataclass
class EnhancedStory:
    """A complete narrative story with progression."""
    title: str
    genre: str
    theme: str
    protagonist: str
    antagonist: str
    goal: str
    
    locations: Dict[str, Dict]  # location_id: {name, purpose, description}
    steps: List[StoryStep]  # Story progression steps
    start_location: str
    end_location: str
    
    # Additional narrative
    world_description: str
    atmosphere: str
    key_objects: List[str]  # Important items for story
    
    # NPC roles (will be filled later)
    npc_roles: Dict[str, str] = field(default_factory=dict)  # location: role


class EnhancedStoryGenerator:
    """Generates complete, coherent stories with narrative progression."""
    
    # Story templates by genre
    STORY_TEMPLATES = {
        "fantasy": {
            "themes": [
                {
                    "name": "Artifact Quest",
                    "template": "The {antagonist} has stolen the {artifact}. Travel to {location} and retrieve it.",
                    "steps": [
                        "Hear rumors in the tavern",
                        "Travel to the forest and find clues",
                        "Discover the ancient temple",
                        "Face the {antagonist} at the artifact location",
                        "Defeat {antagonist} and reclaim the {artifact}",
                    ],
                    "locations_needed": 5,
                },
                {
                    "name": "Rescue Mission",
                    "template": "A {person} has been captured by {antagonist}. Find them and bring them to safety.",
                    "steps": [
                        "Learn about the kidnapping",
                        "Track the {antagonist} through the wilderness",
                        "Find the hidden lair",
                        "Confront the {antagonist}",
                        "Rescue the {person} and return home",
                    ],
                    "locations_needed": 5,
                }
            ],
            "locations": ["Village", "Forest", "Ancient Ruins", "Dark Cave", "Boss Lair"],
            "antagonists": ["Dark Lord", "Evil Sorcerer", "Dragon", "Cursed King"],
            "artifacts": ["Crystal Crown", "Magic Amulet", "Sacred Sword", "Ancient Relic"],
        },
        "scifi": {
            "themes": [
                {
                    "name": "Space Station Crisis",
                    "template": "The {antagonist} AI has taken control of the space station. Restore systems and stop it.",
                    "steps": [
                        "Receive distress call",
                        "Dock at space station",
                        "Investigate lower levels",
                        "Find the AI core",
                        "Override the AI system",
                    ],
                    "locations_needed": 5,
                },
            ],
            "locations": ["Landing Dock", "Cargo Bay", "Medical Lab", "Engineering", "AI Core"],
            "antagonists": ["Rogue AI", "AI Overlord", "Infected AI", "Corrupted Mainframe"],
        },
        "detective": {
            "themes": [
                {
                    "name": "Murder Mystery",
                    "template": "A {victim} has been murdered. Find clues and identify the {antagonist}.",
                    "steps": [
                        "Arrive at crime scene",
                        "Interview witnesses",
                        "Search for evidence",
                        "Confront suspects",
                        "Identify and catch the murderer",
                    ],
                    "locations_needed": 5,
                },
            ],
            "locations": ["Crime Scene", "Police Station", "Bar", "Apartment", "Warehouse"],
            "antagonists": ["Serial Killer", "Corrupt Official", "Smuggler", "Crime Boss"],
        },
        "horror": {
            "themes": [
                {
                    "name": "Haunted Location",
                    "template": "A {location} is haunted by {antagonist}. Find a way to stop it.",
                    "steps": [
                        "Arrive at the haunted place",
                        "Experience supernatural events",
                        "Uncover the tragedy",
                        "Find the source of haunting",
                        "Banish the {antagonist}",
                    ],
                    "locations_needed": 5,
                },
            ],
            "locations": ["Haunted Mansion", "Graveyard", "Crypt", "Ritual Chamber", "Portal"],
            "antagonists": ["Ghost", "Demon", "Ancient Evil", "Vengeful Spirit"],
        },
    }
    
    @classmethod
    def generate_complete_story(
        cls,
        genre: str,
        keywords: List[str],
        protagonist: str
    ) -> EnhancedStory:
        """Generate a complete story with locations and progression."""
        
        # Get template for genre
        template_dict = cls.STORY_TEMPLATES.get(genre.lower(), cls.STORY_TEMPLATES["fantasy"])
        theme_template = random.choice(template_dict["themes"])
        
        # Generate story basics
        antagonist = random.choice(template_dict["antagonists"])
        locations_list = template_dict["locations"][:5]
        
        # Build story
        story = EnhancedStory(
            title=f"The {theme_template['name']} of {antagonist}",
            genre=genre.lower(),
            theme=theme_template["name"],
            protagonist=protagonist,
            antagonist=antagonist,
            goal=f"Stop {antagonist} and bring peace to the land",
            
            locations={},
            steps=[],
            start_location=locations_list[0],
            end_location=locations_list[-1],
            
            world_description=f"A {genre} world threatened by {antagonist}",
            atmosphere="Dark and mysterious",
            key_objects=[antagonist, "Ancient Artifact", "Magic Key"],
        )
        
        # Create locations from template
        for i, loc_name in enumerate(locations_list):
            story.locations[f"loc_{i}"] = {
                "name": loc_name,
                "purpose": f"Important location in the {theme_template['name']}",
                "description": f"You find yourself in {loc_name}. The air feels charged with mystery.",
                "connections": {},  # Will be set by map generator
            }
        
        # Create story steps
        for i, step_template in enumerate(theme_template["steps"]):
            step = StoryStep(
                id=f"step_{i}",
                title=step_template,
                description=step_template,
                location_ids=[f"loc_{min(i, len(locations_list)-1)}"],
                is_optional=(i < len(theme_template["steps"]) - 1 and random.random() < 0.3),
            )
            story.steps.append(step)
        
        # Mark last step as victory condition
        if story.steps:
            story.steps[-1].title = f"Defeat {antagonist}"
            story.steps[-1].description = f"You must defeat {antagonist} to complete your quest."
        
        return story
    
    @classmethod
    def get_next_steps(cls, story: EnhancedStory, current_step_id: str) -> List[str]:
        """Get the next steps from current position."""
        for i, step in enumerate(story.steps):
            if step.id == current_step_id:
                return [s.title for s in story.steps[i+1:min(i+3, len(story.steps))]]
        return [story.steps[-1].title] if story.steps else []
    
    @classmethod
    def get_step_locations(cls, story: EnhancedStory, step_id: str) -> List[str]:
        """Get locations where a story step occurs."""
        for step in story.steps:
            if step.id == step_id:
                return step.location_ids
        return []
