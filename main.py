from character.character import Character

armion = Character('Armion')
missing_items = {}
print(armion.can_craft('sticky_sword', 1, missing_items))
print(missing_items)