"""Main game controller for the rewritten adventure game."""

import sys
sys.path.insert(0, ".")

from src.dynamic_ascii import DynamicASCII
from src.new_game_engine import NewAdventure
from src.item_system import ItemFactory, Item, ItemType


class Game:
    """Game controller."""
    
    GENRES = ["fantasy", "scifi", "detective", "horror"]
    
    def __init__(self):
        self.adventure: NewAdventure = None
    
    def show_welcome(self):
        """Show welcome banner."""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                  CLI ADVENTURE GAME (v2.0)                   ║
║              A Dynamic Text-Based Adventure                  ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        print(DynamicASCII.get_location_art("castle"))
    
    def get_player_name(self) -> str:
        """Get player name."""
        while True:
            name = input("\nWhat is your name, adventurer? ").strip()
            if name and 1 <= len(name) <= 30:
                return name
            print("Please enter a valid name (1-30 characters).")
    
    def get_genre(self) -> str:
        """Get preferred genre."""
        print("\n📖 Choose your adventure type:\n")
        for i, genre in enumerate(self.GENRES, 1):
            print(f"  {i}. {genre.capitalize()}")
        
        while True:
            choice = input("\nEnter number or genre name: ").strip().lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.GENRES):
                    return self.GENRES[idx]
            
            if choice in self.GENRES:
                return choice
            
            print("Invalid choice. Try again.")
    
    def get_keywords(self) -> list:
        """Get story keywords."""
        keywords_str = input("\nEnter story keywords (comma-separated, e.g., 'magic, dragons, prophecy'): ").strip()
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
        return keywords if keywords else ["adventure"]
    
    def get_encounters_preference(self) -> bool:
        """Ask if player wants encounters enabled."""
        while True:
            choice = input("\nEnable combat encounters? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            if choice in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'.")
    
    def start_new_game(self):
        """Initialize a new game."""
        self.show_welcome()
        
        player_name = self.get_player_name()
        genre = self.get_genre()
        keywords = self.get_keywords()
        encounters = self.get_encounters_preference()
        
        self.adventure = NewAdventure(player_name)
        self.adventure.initialize_game(genre, keywords, encounters)
        
        print(f"\n{'='*60}")
        print(f"Welcome, {player_name}!")
        print(f"{'='*60}\n")
        print(f"Story: {self.adventure.story.title}")
        print(f"Goal: {self.adventure.story.protagonist_goal}")
        print(f"Keywords: {', '.join(self.adventure.story.keywords)}")
        print(f"Combat Encounters: {'Enabled' if encounters else 'Disabled'}")
        print(f"\nType 'help' for commands.\n")
    
    
    def run_game_loop(self):
        """Main game loop."""
        while self.adventure.is_running():
            try:
                command = input("➜ ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ["quit", "exit"]:
                    print("\nThanks for playing!")
                    break
                
                response = self.adventure.process_command(command)
                print(response)
                
                # Show ASCII art occasionally
                if self.adventure.turn_count % 8 == 0:
                    print("\n" + DynamicASCII.get_random_art())
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
        
        # Check if story completed
        if self.adventure.state.name == "VICTORY":
            self.show_victory()
        elif self.adventure.state.name == "DEFEAT":
            self.show_defeat()
    
    def show_victory(self):
        """Show victory screen."""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                         🏆 VICTORY 🏆                         ║
║                                                               ║
║              You have completed your quest!                  ║
║         The world has been saved by your bravery.           ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        print(f"Final Stats:")
        print(f"  Turns: {self.adventure.turn_count}")
        print(f"  Health: {self.adventure.player.health}/{self.adventure.player.max_health}")
        print(f"  Locations: {len(set(loc.name for loc in self.adventure.map.locations.values() if loc.visited))}")
    
    def show_defeat(self):
        """Show defeat screen."""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                        💀 DEFEAT 💀                           ║
║                                                               ║
║            You have fallen in your adventure.                ║
║                Better luck next time...                      ║
╚═══════════════════════════════════════════════════════════════╝
        """)
    
    def run(self):
        """Run the game."""
        self.start_new_game()
        self.run_game_loop()


def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
