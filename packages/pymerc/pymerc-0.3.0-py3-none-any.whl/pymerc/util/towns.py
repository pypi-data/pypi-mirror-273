import math

from pymerc.api.models.towns import TownData
from pymerc.client import Client

def calculate_town_satisfaction(data: TownData):
    """Calculate the satisfaction of a town.

    Args:
        data (TownData): The data for the town

    Returns:
        int: The satisfaction of the town
    """
    demands = sum([category.products for category in data.commoners.sustenance], [])
    desire_total = sum(demand.desire for demand in demands)
    result_total = sum(demand.result for demand in demands)

    return math.ceil((result_total / desire_total) * 100)

async def get_towns_market_data(client: Client):
    """Get the market data for all towns.

    Args:
        client (Client): The client to use for the request

    Returns:
        dict: The market data for all towns
    """
    market_data = {}
    towns = await client.towns.get_all()
    for town in towns:
        market_data[town.name] = await client.towns.get_market_data(town.id)

    return market_data


def sum_town_structures(data: TownData):
    """Sum the structures in a town.

    Args:
        data (TownData): The data for the town

    Returns:
        int: The sum of the structures in the town
    """
    return len([domain for domain in data.domain.values() if domain.structure is not None])

def sum_town_taxes(data: TownData):
    """Sum the taxes collected by a town.

    Args:
        data (TownData): The data for the town

    Returns:
        int: The sum of the taxes collected by the town
    """
    return sum(tax for tax in data.government.taxes_collected.__dict__.values())
