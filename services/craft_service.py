from tools.waitable import Waitable
from character.character_model import CharacterModel
from connexion import Connexion
from tools.server import Server
from items import item_factory
from items.items_handler import ItemsHandler

import dpath

class CraftService(Waitable):
    def __init__(self, model: CharacterModel) -> None:
        self.model = model
        self.connexion = Connexion()
        self.server = Server()


    def crafting_skill(self, item_code: str) -> str:
        ih = ItemsHandler()
        item = ih.find_item(item_code, item_factory)

        return item.recipe.skill

    def craft(self, item_code: str, amount: int = 1) -> None:
        data = {'components': {}, 'skills': {}}
        
        if not self.is_craftable(item_code, amount, data):
            print(f"impossible to craft the item. missing requirements: {data}")
            return None
        
        self.wait_for_cd()
        print("Starting crafting")

        self.model.update_data(
            dpath.util.get(self.__query_craft(item_code, amount), 'data/character')
        )

    def is_craftable(self,item_code: str, amount: int = 1, missing_items: dict = None) -> bool:
        if not missing_items:
            missing_items = {'components': {}, 'skills': {}}
        ih = ItemsHandler()
        item = ih.find_item(item_code, item_factory)
        result = True

        self.__add_missing_skill(missing_items.get('skills'), item)

        if not item.has_recipe():
            self.__add_missing_items(missing_items.get('components'), item.code, amount)
            return False
        
        for component in item.recipe.components:
            required_amount = self.model.missing_item(component.code, component.amount * amount)
            if required_amount >= 1:
                result = self.__compute_missing__components(component, missing_items, result, required_amount)
        
        return result
    
    def __compute_missing__components(self, component, missing_items, result, required_amount = 1) -> bool:
        if component.has_recipe():
            result = self.is_craftable(component.code, required_amount, missing_items) and False
        else:
            result = False
            self.__add_missing_items(missing_items.get('components'), component.code, required_amount)
        return result
    
    def __add_missing_items(self, missing_items, item_code, amount) -> None:
        if missing_items.get(item_code) is not None:
            missing_items[item_code] = missing_items.get(item_code) + amount
        else:
            missing_items[item_code] = amount
        
        return None
    
    def __add_missing_skill(self, missing_skill, item):
        craft_lvl = self.model.skill(item.recipe.skill).get('lvl')
        if craft_lvl < item.recipe.lvl:
            missing_skill[item.recipe.skill] = max(missing_skill.get(item.recipe.skill) or 1, item.recipe.lvl)

        return None

    def __query_craft(self, item_code: str, amount: int = 1) -> None:
        return self.connexion.post(
                    f"my/{self.model.character_name}/action/crafting",
                    self.__query_body(item_code, amount)
                )

    def __query_body(self, item_code: str, amount: str = 1) -> dict:
        return {
            'code': item_code,
            'quantity': amount
        }