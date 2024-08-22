from tools.data_handler import DataHandler

class ItemsHandler(DataHandler):
    def __init__(self, source="offline"):
        if source == "offline":
            self.offline_load('data/items.json')
        else:
            self.online_load('items')
    
    def find_item(self, code: str, item_factory):
        for item_data in self.data['data']:
            if item_data['code'] is not None and item_data.get('code') == code:
                return item_factory(item_data)
        return None