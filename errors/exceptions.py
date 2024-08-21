class CharacterNotFoundError(Exception):
    def __init__(self, character_name):
        self.character_name = character_name
        super().__init__(f"Character '{self.character_name}' not found.")

    def __str__(self):
        return f"Character '{self.character_name}' not found."

class CooldownNotReady(Exception):
    def __init__(self):
        super().init("The cooldown is still in progress")
    
    def __str__(self):
        "The cooldown is still in progress"

class CharacterLocked(Exception):
    def __init__(self):
        super().init("The character is locked")
    
    def __str__(self):
        "The character is locked"

class InventoryFull(Exception):
    def __init__(self):
        super().init("The inventory is full !")
    
    def __str__(self):
        "The inventory is full !"

class ServerUnavailable(Exception):
    def __init__(self):
        super().init("The server is currently unavailable")
    
    def __str__(self):
        "The server is currently unavailable"