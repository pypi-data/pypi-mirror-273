from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class Building(BaseModel):
    """Represents a building in the game."""
    type: str
    supports_boost: Optional[bool] = False
    requires: BuildingRequirements
    construction: Optional[BuildingConstruction] = None
    upgrades: Optional[list[BuildingUpgrade]] = []


class BuildingRequirements(BaseModel):
    """Represents the requirements for a building."""
    fertility: Optional[TileRequirement] = None
    forest: Optional[TileRequirement] = None
    climate: Optional[str] = None


class TileRequirement(BaseModel):
    """Represents a requirement for a tile."""
    min: Optional[int] = None
    max: Optional[int] = None


class BuildingRequirement(BaseModel):
    """Represents a requirement for a building."""
    center: Optional[bool] = False
    climate: Optional[str] = None
    min: Optional[int] = None
    resource: Optional[str] = None

class BuildingConstruction(BaseModel):
    """Represents the construction requirements for a building."""
    range: Optional[int] = None
    size: Optional[int] = None
    discount: Optional[int] = None
    time: int
    materials: dict[str, int]

class BuildingUpgrade(BaseModel):
    """Represents an upgrade for a building."""
    type: str
    construction: BuildingConstruction

class Recipe(BaseModel):
    """Represents a recipe for a product in the game."""
    name: str
    tier: int
    building: str
    size: int
    product_class: Optional[str] = Field(alias='class', default=None)
    points: Optional[float] = None
    inputs: Optional[list[Ingredient]] = []
    outputs: Optional[list[Ingredient]] = []


class Ingredient(BaseModel):
    """Represents an ingredient in a recipe."""
    product: str
    amount: float

class Transport(BaseModel):
    """Represents a transport in the game."""
    type: str
    category: int
    tier: int
    capacity: int
    speed: int
    journey_duration: int
    effective_days: int
    operating_costs: dict[str, float]
    catches: Optional[str] = None
    fishing_range: Optional[int] = None

class Item(BaseModel):
    """Represents an item in the game."""
    name: str
    type: str
    unit: str
    weight: Optional[float] = None
    tier: int
    classes: Optional[list[str]] = []
    price: ItemPrice

class ItemPrice(BaseModel):
    """Represents the price of an item in the game."""
    low: float
    typical: float
    high: float