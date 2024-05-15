from pymerc.api.base import BaseAPI
from pymerc.api.models import player


BASE_URL = "https://play.mercatorio.io/api/player"

class PlayerAPI(BaseAPI):
    """A class for interacting with the player API endpoint."""

    async def get(self) -> player.Player:
        """Get data for the player.

        Returns:
            Player: The data for the player
        """
        response = await self.client.get(BASE_URL)
        return player.Player.model_validate(response.json())