"""NPC interaction system - talk, trade, clue, unlock."""

from typing import Optional, List, Dict
from dataclasses import dataclass, field
from enum import Enum


class NPCType(Enum):
    """Types of NPCs."""
    MERCHANT = "merchant"
    GUARD = "guard"
    ALLY = "ally"
    VILLAIN = "villain"
    QUEST_GIVER = "quest_giver"
    NEUTRAL = "neutral"


@dataclass
class DialogueOption:
    """A dialogue choice for the player."""
    text: str
    response: str
    unlocks: Optional[str] = None  # Path/location this unlocks
    gives_item: Optional[str] = None
    gives_clue: Optional[str] = None


@dataclass
class NPC:
    """A non-player character."""
    name: str
    npc_type: NPCType
    description: str
    greeting: str
    dialogue_options: List[DialogueOption] = field(default_factory=list)
    inventory: List[str] = field(default_factory=list)  # Items NPC has
    has_been_talked_to: bool = False
    is_hostile: bool = False
    location_id: Optional[str] = None


class NPCFactory:
    """Factory for creating NPCs."""
    
    NPC_TEMPLATES = {
        "fantasy": {
            "Wise Wizard": {
                "type": NPCType.QUEST_GIVER,
                "description": "An elderly wizard with a long beard",
                "greeting": "Greetings, traveler. I sense great destiny about you.",
                "dialogue": [
                    DialogueOption("What's happening here?", "Dark forces are stirring. You must stop the Dark Lord before it's too late.", gives_clue="Dark Lord's weakness"),
                    DialogueOption("Can you help me?", "I can provide guidance, but the victory must be yours.", gives_item="Magic Scroll"),
                ]
            },
            "Brave Knight": {
                "type": NPCType.ALLY,
                "description": "A seasoned warrior in shining armor",
                "greeting": "Well met! I'd be honored to aid you in your quest.",
                "dialogue": [
                    DialogueOption("Will you join me?", "Aye, I shall fight beside you.", gives_clue="Enemy patrol routes"),
                    DialogueOption("What do you know?", "The castle ahead is well-guarded. Be cautious.", gives_clue="Guard positions"),
                ]
            },
        },
        "scifi": {
            "AI Assistant": {
                "type": NPCType.ALLY,
                "description": "A holographic artificial intelligence",
                "greeting": "Greetings. I am here to assist you.",
                "dialogue": [
                    DialogueOption("What's the situation?", "The station is under siege. We must restore power.", gives_clue="Power core location"),
                    DialogueOption("Can you help?", "I can provide system access if you need it.", gives_item="Access Card"),
                ]
            },
        },
        "detective": {
            "Police Captain": {
                "type": NPCType.QUEST_GIVER,
                "description": "A gruff police captain",
                "greeting": "Detective, glad you're on the case.",
                "dialogue": [
                    DialogueOption("What do we know?", "Three bodies, same location. Pattern suggests a serial killer.", gives_clue="Killer's MO"),
                    DialogueOption("Any leads?", "Check the warehouse district. Suspects were last seen there.", gives_clue="Warehouse location"),
                ]
            },
        },
        "horror": {
            "Priest": {
                "type": NPCType.ALLY,
                "description": "A holy man with a sacred symbol",
                "greeting": "The darkness here is strong. You will need protection.",
                "dialogue": [
                    DialogueOption("What can you tell me?", "An ancient curse binds this place. It must be broken.", gives_clue="Curse ritual"),
                    DialogueOption("Will you help?", "I will perform a blessing to aid you.", gives_item="Holy Water"),
                ]
            },
        },
    }
    
    @classmethod
    def create_npc(cls, genre: str, npc_name: str) -> Optional[NPC]:
        """Create an NPC from template."""
        templates = cls.NPC_TEMPLATES.get(genre.lower(), {})
        template = templates.get(npc_name)
        
        if not template:
            return None
        
        # Handle both DialogueOption objects and dicts
        dialogue_options = []
        for d in template.get("dialogue", []):
            if isinstance(d, DialogueOption):
                dialogue_options.append(d)
            else:
                dialogue_options.append(
                    DialogueOption(d.get("text", ""), d.get("response", "..."), 
                                  d.get("unlocks"), d.get("gives_item"), d.get("gives_clue"))
                )
        
        return NPC(
            name=npc_name,
            npc_type=template.get("type", NPCType.NEUTRAL),
            description=template.get("description", ""),
            greeting=template.get("greeting", "Hello."),
            dialogue_options=dialogue_options,
        )
    
    @classmethod
    def get_npcs(cls, genre: str) -> list:
        """Get NPC instances for a genre."""
        templates = cls.NPC_TEMPLATES.get(genre.lower(), cls.NPC_TEMPLATES.get("fantasy", {}))
        npcs = []
        for npc_name in templates.keys():
            npc = cls.create_npc(genre, npc_name)
            if npc:
                npcs.append(npc)
        return npcs


class NPCInteraction:
    """Handles NPC interactions."""
    
    @staticmethod
    def talk_to_npc(npc: NPC) -> Dict:
        """Talk to an NPC."""
        if npc.is_hostile:
            return {
                "success": False,
                "message": f"The {npc.name} is hostile and won't talk to you.",
            }
        
        npc.has_been_talked_to = True
        return {
            "success": True,
            "message": npc.greeting,
            "dialogue_options": [
                f"{i+1}. {opt.text}"
                for i, opt in enumerate(npc.dialogue_options)
            ],
        }
    
    @staticmethod
    def choose_dialogue(npc: NPC, option_index: int) -> Dict:
        """Choose a dialogue option."""
        if option_index < 0 or option_index >= len(npc.dialogue_options):
            return {"success": False, "message": "Invalid choice."}
        
        option = npc.dialogue_options[option_index]
        return {
            "success": True,
            "response": option.response,
            "gives_item": option.gives_item,
            "gives_clue": option.gives_clue,
            "unlocks": option.unlocks,
        }
