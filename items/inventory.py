from items.item import Item

class Inventory:
    def __init__(self, data = None):
        if data != None :
            self.load_from_data(data)
    
    def load_from_data(self, data):
        self.size = data['inventory_max_items']

        self.slots = []
        for item in data['inventory'] :
            self.slots.append(Item(item))
        
        self.items_amount = sum(item.quantity for item in self.slots)