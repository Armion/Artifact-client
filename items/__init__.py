from items.item import Item

def item_factory(data: dict) -> Item:
    return Item(data)

