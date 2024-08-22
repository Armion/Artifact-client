from items.item import Item
from items.items_handler import ItemsHandler

class Recipe:
    def __init__(self, data = None) -> None:
        self.data = data
        self.load_from_data()

    def load_from_data(self, data: dict = None) -> None:
        if data is None:
            data = self.data

        ih = ItemsHandler()
        
        self.skill = data.get('skill')
        self.lvl = data.get('level')
        self.items = [
            ih.find_item(item.get('code'))
            for item in data.get('items')
        ]
