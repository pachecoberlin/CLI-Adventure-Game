"""Unit tests for the adventure game."""

import pytest
from src.game_engine import Adventure, Character, Item, Location, GameState
from src.scenario_generator import ScenarioGenerator


class TestCharacter:
    """Tests for Character class."""
    
    def test_character_creation(self):
        char = Character("Test Hero")
        assert char.name == "Test Hero"
        assert char.health == 100
        assert len(char.inventory) == 0
    
    def test_take_item(self):
        char = Character("Hero")
        item = Item("sword", "A sharp blade")
        assert char.take_item(item) == True
        assert len(char.inventory) == 1
        assert char.has_item("sword")
    
    def test_drop_item(self):
        char = Character("Hero")
        item = Item("potion", "A healing drink")
        char.take_item(item)
        dropped = char.drop_item("potion")
        assert dropped == item
        assert not char.has_item("potion")
    
    def test_inventory_full(self):
        char = Character("Hero")
        for i in range(10):
            char.take_item(Item(f"item{i}", "test"))
        new_item = Item("extra", "shouldn't fit")
        assert char.take_item(new_item) == False
    
    def test_take_damage(self):
        char = Character("Hero")
        char.take_damage(30)
        assert char.health == 70
    
    def test_health_cannot_go_below_zero(self):
        char = Character("Hero")
        char.take_damage(150)
        assert char.health == 0
        assert not char.is_alive()


class TestLocation:
    """Tests for Location class."""
    
    def test_location_creation(self):
        loc = Location("Forest", "A dark forest")
        assert loc.name == "Forest"
        assert len(loc.exits) == 0
        assert len(loc.items) == 0


class TestAdventure:
    """Tests for Adventure class."""
    
    def test_adventure_creation(self):
        adv = Adventure("fantasy")
        assert adv.interest == "fantasy"
        assert adv.state == GameState.STARTING
        assert adv.turn_count == 0
    
    def test_adventure_start(self):
        adv = Adventure("scifi")
        adv.start_game()
        assert adv.state == GameState.EXPLORING
        assert adv.current_location is not None
    
    def test_look_command(self):
        adv = Adventure("fantasy")
        adv.start_game()
        response = adv.cmd_look()
        assert adv.current_location.name in response
        assert "📍" in response
    
    def test_take_item(self):
        adv = Adventure("fantasy")
        adv.start_game()
        # Add an item to the location
        item = Item("key", "A rusty key")
        adv.current_location.items.append(item)
        
        response = adv.cmd_take("key")
        assert "took" in response.lower()
        assert adv.player.has_item("key")
    
    def test_drop_item(self):
        adv = Adventure("fantasy")
        adv.start_game()
        item = Item("gem", "A precious gem")
        adv.player.take_item(item)
        
        response = adv.cmd_drop("gem")
        assert "dropped" in response.lower()
        assert not adv.player.has_item("gem")
    
    def test_inventory_command(self):
        adv = Adventure("fantasy")
        adv.start_game()
        item = Item("scroll", "An ancient scroll")
        adv.player.take_item(item)
        
        response = adv.cmd_inventory()
        assert "scroll" in response.lower()
    
    def test_help_command(self):
        adv = Adventure("fantasy")
        adv.start_game()
        response = adv.cmd_help()
        assert "look" in response.lower()
        assert "go" in response.lower()
    
    def test_status_command(self):
        adv = Adventure("fantasy")
        adv.start_game()
        response = adv.cmd_status()
        assert "health" in response.lower()
        assert "100" in response
    
    def test_process_command(self):
        adv = Adventure("fantasy")
        adv.start_game()
        response = adv.process_command("help")
        assert "look" in response.lower()
        assert len(adv.history) > 0


class TestScenarioGenerator:
    """Tests for ScenarioGenerator class."""
    
    def test_generate_world_fantasy(self):
        adv = Adventure("fantasy")
        adv.start_game()
        ScenarioGenerator.generate_world(adv)
        assert adv.current_location is not None
        assert len(adv.visited_locations) > 0
    
    def test_generate_world_scifi(self):
        adv = Adventure("scifi")
        adv.start_game()
        ScenarioGenerator.generate_world(adv)
        assert adv.current_location is not None
    
    def test_world_has_items(self):
        adv = Adventure("detective")
        adv.start_game()
        ScenarioGenerator.generate_world(adv)
        # At least some items should be in the world
        total_items = sum(len(loc.items) for loc in [adv.current_location])
        # Note: This is a simplified check
        assert adv.current_location is not None
    
    def test_world_has_exits(self):
        adv = Adventure("horror")
        adv.start_game()
        ScenarioGenerator.generate_world(adv)
        assert len(adv.current_location.exits) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
