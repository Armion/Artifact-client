from items.item import Item
from items.recipe import Recipe
from items.items_handler import ItemsHandler



def item_factory(data: dict) -> Item:
    return Item(data)

