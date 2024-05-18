from pydantic import TypeAdapter

from pymerc.api.base import BaseAPI
from pymerc.api.models import map

BASE_URL = "https://play.mercatorio.io/api/map/regions"


class MapAPI(BaseAPI):
    """A class for interacting with the map API endpoint."""

    async def get_all(self):
        """Get a list of all regions in the game.

        Returns:
            RegionsList: A list of all regions in the game
        """
        adapter = TypeAdapter(list[map.Region])
        response = await self.client.get(BASE_URL)
        return adapter.validate_python(response.json())
