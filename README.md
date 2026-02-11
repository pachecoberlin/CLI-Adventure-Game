# CLI Adventure Game - Next Generation

A dynamic, text-based adventure game that generates a unique story and world for each playthrough.

## Features

### 🎮 Core Gameplay
- **Dynamic Story Generation**: Each game creates a unique storyline with themes (Fantasy, Sci-Fi, Detective, Horror)
- **Fixed World Map**: Explore a consistent world with varied routes, dead ends, and special transitions
- **Multi-Round Combat**: Strategic encounters with attack, defend, heal, and flee actions
- **Item Management**: Find, equip, and use items that affect your abilities
- **NPC Interactions**: Talk to characters for clues, items, and story progression

### 🛠️ Systems

#### Story Generation
- Template-based story creation with 4 genres
- Automatic location extraction from story narratives
- Quest tracking and story node progression
- Dynamic antagonist and goal generation

#### Map System
- Fixed routes between locations (not randomly generated)
- Dead ends and varied connections
- Special transitions (teleports, one-way passages, entering locations)
- Location descriptions that vary on first visit vs. revisits

#### Combat System
- Multi-round combat with damage calculation
- Armor-based damage reduction
- Combat actions: Attack, Defend, Heal, Flee
- Enemy variety with different stats
- Victory/Defeat conditions

#### Item System
- Weapons (increase damage)
- Armor (reduce damage taken)
- Healing items (consumable and reusable)
- Quest items (unlock locations)
- Genre-specific item pools

#### Character System
- Player health and healing
- Equipment management (weapon/armor slots)
- Inventory with carrying capacity
- Character statistics

### 🎨 Immersion
- Dynamic ASCII art for locations and creatures
- Genre-appropriate descriptions
- Atmospheric feedback and events
- Encounter system (optional/experimental)

## Getting Started

### Installation

```bash
git clone git@github.com:pachecoberlin/CLI-Adventure-Game.git
cd CLI-Adventure-Game
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Playing the Game

```bash
python src/main.py
```

Follow the prompts to:
1. Enter your character name
2. Choose a genre (Fantasy, Sci-Fi, Detective, Horror)
3. Enter keywords to shape the story
4. Enable/disable combat encounters (experimental feature)

### Commands

While playing:

```
look              - Examine your current location
go <direction>    - Move (north, south, east, west)
take <item>       - Pick up an item
drop <item>       - Drop an item from inventory
inventory         - Show your items
equip <item>      - Equip a weapon or armor
unequip <item>    - Remove equipment
use <item>        - Use an item
talk <npc>        - Talk to someone
inspect <object>  - Look closely at something
status            - Show your character status
story             - Show story progress
help              - Show this help message

[In Combat]
attack            - Attack the enemy
defend            - Brace for impact
heal              - Use a healing item
flee              - Try to escape
```

## Game Design

### Story Modes

Each playthrough generates a story with:
- A protagonist (the player)
- An antagonist (the goal)
- Multiple locations connected by meaningful routes
- Quest objectives and progression

Genres available:
- **Fantasy**: Dragons, magic, quests, curses
- **Sci-Fi**: Space stations, AI, alien worlds, technology
- **Detective**: Crime scenes, clues, suspects, investigations
- **Horror**: Haunted locations, creatures, supernatural events

### Map Design

The world is built with:
- **Locations**: Each location has a description that varies based on visit status
- **Transitions**: Routes between locations with different types (normal, enter, teleport, one-way)
- **Items**: Found scattered throughout the world
- **NPCs**: Characters to interact with for information and rewards

### Combat

Combat is tactical:
1. **Attack**: Deal damage to enemy (damage = weapon bonus ± variance)
2. **Defend**: Reduce damage taken this round
3. **Heal**: Use a healing item (takes action, doesn't attack)
4. **Flee**: Attempt to escape (60% success rate)

Damage calculation:
```
damage_dealt = base_damage - enemy_armor + random_variance
```

## Architecture

```
src/
  ├── main.py                 # Entry point and game controller
  ├── new_game_engine.py      # Core game loop and state management
  ├── story_generator.py      # Dynamic story creation
  ├── map_system.py           # World structure and navigation
  ├── item_system.py          # Items and equipment
  ├── combat_system.py        # Multi-round combat
  ├── npc_system.py           # NPCs and dialogue
  └── dynamic_ascii.py        # ASCII art generation

tests/
  ├── test_game_run.py        # Basic system tests
  ├── test_combat_scenario.py # Combat mechanics
  ├── test_full_game.py       # Integration testing
  └── complete_playthrough.py # End-to-end playthrough
```

## Testing

Run automated playthroughs:

```bash
# Basic functionality test
python test_game_run.py

# Combat system test
python test_combat_scenario.py

# Full playthrough
python complete_playthrough.py
```

## Current Features (v2.0)

✅ Dynamic story generation
✅ Fixed map with varied routes
✅ Item discovery and equipment
✅ Multi-round combat with mechanics
✅ NPC interactions
✅ Combat encounters (optional)
✅ Character progression tracking
✅ ASCII art generation
✅ Multiple genres

## Planned Features

- [ ] Story endings and victory conditions
- [ ] Advanced NPC dialogue trees
- [ ] Quest tracking system
- [ ] Skill system
- [ ] Save/Load functionality
- [ ] Difficulty levels
- [ ] More detailed ASCII art
- [ ] Sound effects (optional)
- [ ] Expanded genre options

## Development

### Adding a New Genre

1. Add templates to `StoryGenerator.STORY_TEMPLATES`
2. Add weapons/armor/healing to `ItemFactory` templates
3. Add NPCs to `NPCFactory.NPC_TEMPLATES`
4. Add ASCII art to `DynamicASCII`

Example:
```python
# story_generator.py
"your_genre": {
    "themes": ["theme1", "theme2"],
    "locations": ["Location 1", "Location 2"],
    # ... more templates
}
```

## Contributing

Issues and pull requests are welcome!

## License

This project is part of the GitHub Copilot CLI demonstration.

## Changelog

### v2.0 (Current)
- Complete engine rewrite
- Story generation system
- Fixed map with varied transitions
- Combat mechanics overhaul
- NPC system implementation
- Item system with equipment
- ASCII art generation

### v1.0
- Initial MVP with basic exploration
- Simple combat
- Random map generation

---

**Enjoy your adventure!** 🗡️ 🐉 ✨

## Story Completion System

The game features a **story completion system** where defeating a boss enemy triggers a story victory.

### How to Reach Victory
1. **Explore the world** - Navigate through different locations
2. **Collect items** - Find weapons, armor, and healing items
3. **Prepare for combat** - Equip the best gear available
4. **Defeat the Boss** - After turn 40+, you may encounter the final boss
5. **Victory!** - Defeating the boss completes the story

### Boss Mechanics
- Boss appears after ~40 turns of gameplay
- Boss has 80 HP vs. regular enemies' 30 HP
- Boss deals 15 damage vs. regular enemies' 8 damage  
- Boss has higher armor (5) vs. regular enemies' (2)
- Defeating the boss triggers a story ending screen

### Winning Strategy
- Collect healing items throughout the game
- Equip the strongest weapon you find
- Equip armor to reduce incoming damage
- Use defend action to reduce damage further
- Use healing strategically during boss fight

## Version History

### v2.0 (Current - Feature Complete)
✅ Dynamic story generation
✅ Fixed map with varied transitions
✅ Combat system with full mechanics
✅ Item discovery and equipment
✅ NPC interaction framework
✅ Optional combat encounters
✅ Story ending with boss defeat
✅ ASCII art generation
✅ Multi-genre support (4 genres)

### Features Confirmed Working
- Story generation works for all 4 genres
- Combat system fully functional with all actions
- Equipment bonuses properly calculated
- Boss encounters detectable and defeatable
- Game completion verified through testing

---

**Ready to Play!** 🎮
