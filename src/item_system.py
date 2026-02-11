"""Item system with weapons, armor, healing, and special properties."""

from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    """Types of items in the game."""
    WEAPON = "weapon"
    ARMOR = "armor"
    HEALING = "healing"
    KEY = "key"  # Unlocks locations
    QUEST = "quest"  # Quest-related item
    CONSUMABLE = "consumable"  # One-use item


@dataclass
class Item:
    """An item that can be collected and used."""
    name: str
    description: str
    item_type: ItemType
    
    # Combat properties
    damage_bonus: int = 0  # For weapons
    armor_value: int = 0  # For armor
    healing_amount: int = 0  # For healing items
    
    # Special properties
    unlocks: Optional[str] = None  # Location or path this unlocks
    is_consumable: bool = False  # Item disappears after use
    is_usable: bool = True  # Can be used in inventory
    special_effect: Optional[str] = None  # Special description of effect
    
    def get_full_description(self) -> str:
        """Get detailed description with properties."""
        desc = f"{self.name}: {self.description}\n"
        
        if self.damage_bonus > 0:
            desc += f"  → Damage Bonus: +{self.damage_bonus}\n"
        if self.armor_value > 0:
            desc += f"  → Armor Value: {self.armor_value}\n"
        if self.healing_amount > 0:
            desc += f"  → Healing: +{self.healing_amount} HP\n"
        if self.unlocks:
            desc += f"  → Unlocks: {self.unlocks}\n"
        if self.special_effect:
            desc += f"  → Special: {self.special_effect}\n"
        
        return desc.strip()


class ItemFactory:
    """Factory for creating items."""
    
    WEAPON_TEMPLATES = {
        "fantasy": [
            Item("Iron Sword", "A sturdy steel blade", ItemType.WEAPON, damage_bonus=15),
            Item("Magic Staff", "A glowing staff crackling with power", ItemType.WEAPON, damage_bonus=25, special_effect="Deals magical damage"),
            Item("Ancient Axe", "A legendary weapon", ItemType.WEAPON, damage_bonus=20),
        ],
        "scifi": [
            Item("Laser Pistol", "Compact energy weapon", ItemType.WEAPON, damage_bonus=12),
            Item("Plasma Rifle", "Advanced energy rifle", ItemType.WEAPON, damage_bonus=20),
            Item("Ion Cannon", "Heavy weapon", ItemType.WEAPON, damage_bonus=30),
        ],
        "detective": [
            Item("Revolver", "Standard detective sidearm", ItemType.WEAPON, damage_bonus=10),
            Item("Shotgun", "Powerful firearm", ItemType.WEAPON, damage_bonus=18),
        ],
        "horror": [
            Item("Holy Water", "Effective against evil", ItemType.WEAPON, damage_bonus=10, special_effect="Works on undead"),
            Item("Silver Dagger", "A blessed blade", ItemType.WEAPON, damage_bonus=12),
            Item("Blessed Mace", "A holy weapon", ItemType.WEAPON, damage_bonus=15),
        ],
    }
    
    ARMOR_TEMPLATES = {
        "fantasy": [
            Item("Leather Armor", "Basic protection", ItemType.ARMOR, armor_value=5),
            Item("Iron Plate", "Heavy armor", ItemType.ARMOR, armor_value=15),
            Item("Mithril Armor", "Legendary protection", ItemType.ARMOR, armor_value=25),
        ],
        "scifi": [
            Item("Combat Suit", "Standard armor", ItemType.ARMOR, armor_value=8),
            Item("Reinforced Suit", "Heavy combat armor", ItemType.ARMOR, armor_value=15),
        ],
        "detective": [
            Item("Kevlar Vest", "Bullet-resistant vest", ItemType.ARMOR, armor_value=10),
        ],
        "horror": [
            Item("Protective Talisman", "Reduces supernatural damage", ItemType.ARMOR, armor_value=8),
        ],
    }
    
    HEALING_TEMPLATES = [
        Item("Health Potion", "Restores 30 HP", ItemType.HEALING, healing_amount=30, is_consumable=True),
        Item("Greater Potion", "Restores 60 HP", ItemType.HEALING, healing_amount=60, is_consumable=True),
        Item("Full Heal Spell", "Fully restores health", ItemType.HEALING, healing_amount=100, is_consumable=True),
    ]
    
    @classmethod
    def get_weapons(cls, genre: str) -> list:
        """Get available weapons for a genre."""
        return cls.WEAPON_TEMPLATES.get(genre.lower(), cls.WEAPON_TEMPLATES["fantasy"])
    
    @classmethod
    def get_armor(cls, genre: str) -> list:
        """Get available armor for a genre."""
        return cls.ARMOR_TEMPLATES.get(genre.lower(), cls.ARMOR_TEMPLATES["fantasy"])
    
    @classmethod
    def get_healing_items(cls) -> list:
        """Get available healing items."""
        return cls.HEALING_TEMPLATES.copy()
