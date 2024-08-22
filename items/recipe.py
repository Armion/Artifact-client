from items.items_handler import ItemsHandler

class Recipe:
    def __init__(self, data: dict = None, item_factory = None) -> None:
        self.data = data
        self.item_factory = item_factory
        self.load_from_data()

    def load_from_data(self, data: dict = None) -> None:
        if data is None:
            data = self.data

        ih = ItemsHandler()
        
        self.skill = data.get('skill')
        self.lvl = data.get('level')
        self.items = [
            ih.find_item(item.get('code'), self.item_factory)
            for item in data.get('items')
        ]
