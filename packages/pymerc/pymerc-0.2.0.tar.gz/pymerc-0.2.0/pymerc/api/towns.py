from typing import Optional

from pydantic import TypeAdapter

from pymerc.api.base import BaseAPI
from pymerc.api.models import towns

BASE_URL = "https://play.mercatorio.io/api/towns"

class TownsAPI(BaseAPI):
    """A class for interacting with the towns API endpoint."""

    async def init_cache(self):
        pass

    async def get_all(self) -> list[towns.Town]:
        """Get a list of all towns in the game."""
        adapter = TypeAdapter(list[towns.Town])
        response = await self.client.get(BASE_URL)
        return adapter.validate_python(response.json())

    async def get_data(self, id) -> towns.TownData:
        """Get data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            TownData: The data for the town
        """
        response = await self.client.get(f"{BASE_URL}/{id}")
        return towns.TownData.model_validate(response.json())

    async def get_market_data(self, id) -> towns.TownMarket:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            TownMarket: The market data for the town
        """
        response = await self.client.get(f"{BASE_URL}/{id}/marketdata")
        return towns.TownMarket.model_validate(response.json())

    async def get_market_item(
        self, town_id, item
    ) -> Optional[towns.TownMarketItemDetails]:
        """Get the market overview for an item in a town.

        Args:
            town_id (int): The ID of the town
            item (str): The item to get the overview for

        Returns:
            TownMarketItemDetails: The market overview for the town
        """
        response = await self.client.get(f"{BASE_URL}/{town_id}/markets/{item}")
        return towns.TownMarketItemDetails.model_validate(response.json())