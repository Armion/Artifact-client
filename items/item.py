from tools.colors import apply_color, Color
class Item:
    def __init__(self, data = None):
        if data is not None :
            self.load_from_data(data)

    def load_from_data(self, data):
        self.name = data['code']
        self.slot = data['slot']
        self.quantity = data['quantity']

    def display(self):
        if(self.quantity <= 0):
            return None 
        return apply_color(f"Slot: {self.slot}, Item: {self.name}, Quantity: {self.quantity}", Color.GREEN)