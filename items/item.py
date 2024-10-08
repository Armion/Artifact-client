from items.recipe import Recipe
from items.grand_exchange import GrandExchange

class Item:
    def __init__(self, data: dict = None, item_factory = None):
        if data is not None :
            self.item_factory = item_factory
            self.load_from_data(data)
    
    def load_from_data(self, data):
        self.code = data.get('code')
        self.name = data.get('name')
        self.lvl = data.get('level')
        self.type = data.get('type')
        self.subtype = data.get('subtype')
        if data.get('craft'):
            self.recipe = Recipe(data.get('craft'), self.__class__)
        else:
            self.recipe = None

    def has_recipe(self) -> bool:
        if self.recipe is not None:
            return True
        return False

    def get_sell_price(self) -> float:
        self.sell_price = GrandExchange().find_item(self.code).sell_price

        return self.sell_price