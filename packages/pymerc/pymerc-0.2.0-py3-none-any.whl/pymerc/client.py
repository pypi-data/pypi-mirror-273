import httpx

from pymerc.api.map import MapAPI
from pymerc.api.player import PlayerAPI
from pymerc.api.static import StaticAPI
from pymerc.api.towns import TownsAPI

class Client:
    """A simple API client for the Mercatorio API."""

    session: httpx.AsyncClient
    token: str
    user: str

    map: MapAPI
    player: PlayerAPI
    static: StaticAPI
    towns: TownsAPI

    def __init__(self, user: str, token: str):
        self.session = httpx.AsyncClient(http2=True)
        self.user = user
        self.token = token

        self.session.headers.setdefault("X-Merc-User", self.user)
        self.session.headers.setdefault("Authorization", f"Bearer {self.token}")

        self.map = MapAPI(self)
        self.player = PlayerAPI(self)
        self.static = StaticAPI(self)
        self.towns = TownsAPI(self)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request to the given URL.

        Args:
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.get(url, **kwargs)

    async def close(self):
        await self.session.aclose()
