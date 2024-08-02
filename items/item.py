class Item:
    def __init__(self, data = None):
        if data != None :
            self.load_from_data(data)

    def load_from_data(self, data):
        self.name = data['code']
        self.slot = data['slot']
        self.quantity = data['quantity']