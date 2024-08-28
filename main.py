from character.character import Character

armion = Character('Armion')
missing_items = {}
print(armion.can_craft('cooked_chicken', 15, missing_items))