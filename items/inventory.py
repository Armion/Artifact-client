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
    
    def display(self):
        inventory_info = f"Inventory (Max Size: {self.size}, Current Items: {self.items_amount}):"
        items_info = "\n\t".join(item.display() for item in self.slots if item.display() is not None)
        print(f"{inventory_info}\n\t{items_info}")