from pydantic import BaseModel

class Location(BaseModel):
    """Represents the location of something on the map.

    Attributes:
        x (int): The x coordinate of the location.
        y (int): The y coordinate of the location.
    """

    x: int
    y: int