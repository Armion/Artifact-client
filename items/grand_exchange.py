from tools.data_handler import DataHandler
from items.ge_item import GEItem

class GrandExchange(DataHandler):
    def __init__(self, source="online"):
        if source == "offline":
            self.offline_load('data/grand_exchange.json')
        else:
            self.online_load('ge')
    
    def find_item(self, code: str):
        for item_data in self.data['data']:
            if item_data['code'] is not None and item_data.get('code') == code:
                return GEItem(item_data)
        return None