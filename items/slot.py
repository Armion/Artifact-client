import items
from tools.colors import apply_color, Color
from items.item import Item

class Slot:
    def __init__(self, data = None):
        if data is not None :
            self.load_from_data(data)

    def load_from_data(self, data):
        self.name = data.get('code')
        self.slot = data.get('slot')
        self.quantity = data.get('quantity')
        self.item = Item(data, items.item_factory)

    def display(self):
        if(self.quantity <= 0):
            return None 
        return apply_color(f"Slot: {self.slot}, Item: {self.name}, Quantity: {self.quantity}", Color.GREEN)