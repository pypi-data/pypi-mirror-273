from pydantic import BaseModel


class Center(BaseModel):
    """Represents the center of a region.

    Attributes:
        x (int): The x-coordinate of the center.
        y (int): The y-coordinate of the center.
    """

    x: int
    y: int


class Region(BaseModel):
    """Represents a region in the game.

    Attributes:

        id (int): The unique identifier of the region.
        name (str): The name of the region.
        center (Center): The center of the region.
        size (int): The size of the region.
    """

    id: int
    name: str
    center: Center
    size: int

