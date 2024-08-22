from tools.data_handler import DataHandler
from items.item import Item

class ItemsHandler(DataHandler):
    def __init__(self, source="offline"):
        if source == "offline":
            self.offline_load('data/items.json')
        else:
            self.online_load('items')
    
    def find_item(self, code: str) -> Item:
        for item in self.data['data']:
            if item['code'] is not None and item.get('code') == code:
                return Item(item)
        return None