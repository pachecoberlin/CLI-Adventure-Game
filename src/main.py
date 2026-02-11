"""Main game interface and entry point."""

import sys
from src.ascii_art import WELCOME_BANNER, print_banner, get_random_ascii_art
from src.game_engine import Adventure
from src.scenario_generator import ScenarioGenerator


class Game:
    """Main game controller."""
    
    INTERESTS = ["fantasy", "scifi", "detective", "horror"]
    
    def __init__(self):
        self.adventure: Adventure = None
    
    def welcome(self):
        """Show welcome screen."""
        print(WELCOME_BANNER)
        print(get_random_ascii_art())
    
    def get_player_interest(self) -> str:
        """Ask player for their preferred adventure type."""
        print_banner("Choose Your Adventure Type")
        print("What interests you?\n")
        
        for i, interest in enumerate(self.INTERESTS, 1):
            print(f"{i}. {interest.capitalize()}")
        
        while True:
            try:
                choice = input("\nEnter number (1-4) or type interest: ").strip().lower()
                
                # Handle numeric choice
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.INTERESTS):
                        return self.INTERESTS[idx]
                
                # Handle text choice
                if choice in self.INTERESTS:
                    return choice
                
                print("Invalid choice. Please try again.")
            except KeyboardInterrupt:
                sys.exit(0)
    
    def get_player_name(self) -> str:
        """Ask for player name."""
        while True:
            name = input("\nWhat is your name, adventurer? ").strip()
            if name and len(name) <= 20:
                return name
            print("Please enter a valid name (1-20 characters).")
    
    def start_new_game(self):
        """Initialize a new adventure."""
        interest = self.get_player_interest()
        player_name = self.get_player_name()
        
        self.adventure = Adventure(interest, player_name)
        self.adventure.start_game()
        
        # Generate the world
        ScenarioGenerator.generate_world(self.adventure)
        
        # Show starting message
        print_banner(f"Welcome, {player_name}!")
        print(ScenarioGenerator.get_scenario_description(interest))
        print(get_random_ascii_art())
        print("\nType 'help' for available commands.\n")
    
    def run_game_loop(self):
        """Main game loop."""
        if not self.adventure:
            self.start_new_game()
        
        while self.adventure.is_running():
            try:
                command = input("➜ ").strip()
                
                if not command:
                    continue
                
                # Special quit command
                if command.lower() in ["quit", "exit"]:
                    print("\nThanks for playing!")
                    break
                
                response = self.adventure.process_command(command)
                print(response)
                
                # Show occasional ASCII art
                if self.adventure.turn_count % 5 == 0:
                    print("\n" + get_random_ascii_art())
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
    
    def run(self):
        """Run the game."""
        self.welcome()
        self.run_game_loop()


def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
