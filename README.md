# CLI Adventure Game

An interactive text-based adventure game where each playthrough generates a unique, dynamic story based on your interests.

## Features

- **Dynamic Story Generation**: Each game creates a completely new adventure
- **Multiple Scenarios**: Choose from Fantasy, Sci-Fi, Detective, or Horror themes
- **ASCII Art**: Beautiful ASCII artwork enhances the atmosphere
- **Rich Command System**: Explore, take items, manage inventory, and more
- **Replayability**: No two games are ever the same

## Installation

```bash
# Clone the repository
git clone git@github.com:pachecoberlin/CLI-Adventure-Game.git
cd CLI-Adventure-Game

# Install dependencies
pip install -e ".[dev]"
```

## Running the Game

```bash
python -m src.main
```

## How to Play

1. **Start the game** - You'll be greeted with a welcome screen
2. **Choose your scenario** - Pick from Fantasy, Sci-Fi, Detective, or Horror
3. **Enter your name** - Give your character an identity
4. **Explore and interact** - Use commands to move around and interact with the world

## Available Commands

- `look` - Describe your current surroundings
- `go <direction>` - Move in a direction (north, south, east, west)
- `take <item>` - Pick up an item
- `drop <item>` - Drop an item from your inventory
- `inventory` - Show what you're carrying
- `use <item>` - Use an item
- `status` - Check your health and statistics
- `help` - Show all available commands
- `quit` or `exit` - Exit the game

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
CLI-Adventure-Game/
├── src/
│   ├── main.py              # Entry point and game controller
│   ├── game_engine.py       # Core game logic
│   ├── scenario_generator.py # World generation
│   └── ascii_art.py         # Visual elements
├── tests/
│   └── test_game.py         # Unit tests
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Game Scenarios

### Fantasy
Explore magical forests, dragon lairs, and enchanted castles. Discover ancient artifacts and meet mystical creatures.

### Sci-Fi
Navigate space stations, alien planets, and futuristic cities. Use advanced technology and solve technological mysteries.

### Detective
Investigate crime scenes, interrogate suspects, and uncover clues. Solve the mystery!

### Horror
Survive in haunted mansions, dark forests, and eerie locations. Face your fears and escape the terror.

## Future Enhancements

- [ ] NPC interactions and dialogue
- [ ] Combat system
- [ ] Puzzle solving
- [ ] Item crafting
- [ ] Saving and loading games
- [ ] Difficulty levels
- [ ] More scenarios
- [ ] Achievements and statistics

## License

MIT

## Author

Built with GitHub Copilot CLI
