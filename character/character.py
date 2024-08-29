from character.character_model import CharacterModel

from services.move_service import MoveService
from services.fight_service import FightService
from services.gather_service import GatherService
from services.exchange_service import ExchangeService
from services.craft_service import CraftService


class Character:
    def __init__(self, character_name):
        self.model = CharacterModel(character_name)
        self.model.update_data()
        self.move_service = MoveService(self.model)
        self.fight_service = FightService(self.model)
        self.gather_service = GatherService(self.model)
        self.exchange_service = ExchangeService(self.model)
        self.craft_service = CraftService(self.model)

    def __getattr__(self, attr):
        return getattr(self.model, attr)

    def move(self, x: int, y: int) -> None:
        self.move_service.wait_for_cd()
        self.move_service.move_character(x, y)
        self.model.update_data()

    def gather(self):
        self.gather_service.gather()

    def craft(self, item_code: str, amount: int = 1) -> None:
        data = self.can_craft(item_code, amount)
        self.move_service.travel_to_nearest_object(data.get('skill'))
        self.craft_service.craft(item_code)

    def can_craft(self, item_code: str, amount: int = 1, missing_requirements: dict = None) -> dict:
        if not missing_requirements:
            missing_requirements = {'components': {}, 'skills': {}}

        result = {
            'craftable': self.craft_service.is_craftable(item_code, amount, missing_requirements),
            'skill': self.craft_service.crafting_skill(item_code),
            'missing_requirements': missing_requirements
        }

        return result

    def farm_monster(self, name: str ='chicken') -> None:
        print(f"Moving to the nearest {name} spot !")
        self.move_service.travel_to_nearest_object(name)

        while(True):
            self.fight_service.fight()

    def sell_object(self, code: str, quantity: int = 1) -> None:
        self.move_service.travel_to_nearest_object('grand_exchange')
        self.exchange_service.sell_object(code, quantity)

        return None