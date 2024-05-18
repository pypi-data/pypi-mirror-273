from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymerc.client import Client


class BaseAPI:
    """A base class for interacting with the Mercatorio API.

    Attributes:
        client (Client): The client to use for making requests.
    """

    client: Client

    def __init__(self, client: Client):
        self.client = client
