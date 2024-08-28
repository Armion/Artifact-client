from items.items_handler import ItemsHandler
from items.component import Component

class Recipe:
    def __init__(self, data: dict = None, item_factory = None) -> None:
        self.data = data
        self.item_factory = item_factory
        self.load_from_data()

    def load_from_data(self, data: dict = None) -> None:
        if data is None or data == {}:
            data = self.data
        
        self.skill = data.get('skill')
        self.lvl = data.get('level')
        self.components = [
            self.__get_component__(item.get('code'), item.get('quantity')) for item in data.get('items')
        ]

    def __get_component__(self, item_code: str, amount: int):
        it = ItemsHandler().find_item(item_code, self.item_factory)
        return Component(it, amount)
