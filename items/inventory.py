from items.slot import Slot

class Inventory:
    def __init__(self, data: dict = None) -> None:
        if data != None :
            self.load_from_data(data)
    
    def load_from_data(self, data):
        self.size = data['inventory_max_items']

        self.slots = []
        for slot in data['inventory'] :
            self.slots.append(Slot(slot))
        
        self.items_amount = sum(slot.quantity for slot in self.slots)

    def find_item(self, code: str):
        for slot in self.slots:
            if slot.item.code == code:
                return slot.item
        
        return None
    
    def has_item(self, code: str, amount: int = 1) -> bool:
        for slot in self.slots:
            if slot.item.code == code and slot.quantity >= amount:
                return True
        
        return False
    
    def missing_item(self, code: str, amount: int = 1) -> int:
        if self.has_item(code, amount):
            return 0
        else:
            for slot in self.slots:
                if slot.item.code == code:
                    return amount - slot.quantity
        
        return amount
    
    def display(self):
        inventory_info = f"Inventory (Max Size: {self.size}, Current Items: {self.items_amount}):"
        items_info = "\n\t".join(slot.display() for slot in self.slots if slot.display() is not None)
        print(f"{inventory_info}\n\t{items_info}")