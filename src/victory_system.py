"""Victory and story completion system."""

import random
from enum import Enum


class VictoryType(Enum):
    """Types of victory conditions."""
    DEFEAT_ANTAGONIST = "defeat_antagonist"
    COMPLETE_QUEST = "complete_quest"
    ESCAPE = "escape"
    RESCUE = "rescue"


class StoryCompletion:
    """Handles story completion and endings."""
    
    ENDINGS = {
        "fantasy": [
            "With the {antagonist} defeated, peace returns to the land. The {protagonist} is hailed as a hero.",
            "The {antagonist}'s power is broken! The {protagonist} claims the {reward} and ends the curse.",
            "Victory! The {protagonist} has saved the kingdom from {antagonist}'s darkness.",
        ],
        "scifi": [
            "The {antagonist} is destroyed! The {protagonist} saves the colony and returns as a hero.",
            "With {antagonist} defeated, the station is secured. The {protagonist} has saved humanity.",
            "Victory! The {protagonist} has prevented the {antagonist}'s plans and restored peace.",
        ],
        "detective": [
            "The {antagonist} is caught! Justice is served, thanks to the {protagonist}'s investigation.",
            "The {protagonist} has solved the case! {antagonist} faces justice for their crimes.",
            "With {antagonist} captured, peace is restored. The {protagonist} closes the case.",
        ],
        "horror": [
            "The {antagonist} is vanquished! The {protagonist} has ended the nightmare.",
            "With {antagonist} defeated, the darkness lifts. The {protagonist} is finally safe.",
            "Victory! The {protagonist} has survived and conquered the {antagonist}.",
        ],
    }
    
    @staticmethod
    def get_ending(genre: str, protagonist: str, antagonist: str, reward: str) -> str:
        """Generate an ending message."""
        endings = StoryCompletion.ENDINGS.get(genre, StoryCompletion.ENDINGS["fantasy"])
        ending = random.choice(endings)
        
        return ending.format(
            protagonist=protagonist,
            antagonist=antagonist,
            reward=reward
        )
    
    @staticmethod
    def show_victory_screen(game):
        """Show the victory screen."""
        print("""
╔════════════════════════════════════════════════════════════════╗
║                   🏆 VICTORY 🏆                                ║
║                                                                ║
║              You have completed your quest!                   ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        ending_text = StoryCompletion.get_ending(
            game.story.theme,
            game.player.name,
            game.story.protagonist_goal.split("Stop ")[1].split(" ")[0] if "Stop " in game.story.protagonist_goal else "the enemy",
            game.story.protagonist_goal.split("and claim the ")[1] if "and claim the " in game.story.protagonist_goal else "victory"
        )
        
        print(ending_text)
        
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║                     FINAL STATISTICS                          ║
╠════════════════════════════════════════════════════════════════╣
║ Character:      {game.player.name:<50} ║
║ Final Health:   {game.player.health}/{game.player.max_health} HP<{' ' * (43 - len(str(game.player.health)) - len(str(game.player.max_health)))}║
║ Total Turns:    {game.turn_count:<50} ║
║ Items Collected:{len(game.player.inventory):<50} ║
║ Difficulty:     {'Encounters: ' + ('Enabled' if game.encounters_enabled else 'Disabled'):<50} ║
╚════════════════════════════════════════════════════════════════╝

        """)
    
    @staticmethod
    def show_defeat_screen(game):
        """Show the defeat screen."""
        print("""
╔════════════════════════════════════════════════════════════════╗
║                    💀 DEFEAT 💀                                ║
║                                                                ║
║            You have fallen in your quest...                   ║
║              Better luck next time, adventurer.              ║
╚════════════════════════════════════════════════════════════════╝
        """)
