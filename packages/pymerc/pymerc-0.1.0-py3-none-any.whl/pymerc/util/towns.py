import math

from pymerc.api.models.towns import TownData

def sum_town_taxes(data: TownData):
    """Sum the taxes collected by a town.

    Args:
        data (TownData): The data for the town

    Returns:
        int: The sum of the taxes collected by the town
    """
    return sum(tax for tax in data.government.taxes_collected.__dict__.values())

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