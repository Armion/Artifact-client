from connexion import Connexion
from tools.server import Server
from character.character_model import CharacterModel

from services.move_service import MoveService
from services.fight_service import FightService
from services.gather_service import GatherService

import dpath
from time import sleep
from tqdm import tqdm

class Character:
    def __init__(self, character_name):
        self.model = CharacterModel(character_name)
        self.connexion = Connexion()
        self.server = Server()
        self.model.update_data()
        self.move_service = MoveService(self.model)
        self.fight_service = FightService(self.model)
        self.gather_service = GatherService(self.model)

    def move(self, x: int, y: int) -> None:
        self.move_service.wait_for_cd()
        self.move_service.move_character(x, y)
        self.model.update_data()

    def gather(self):
        self.gather_service.gather()

    def farm_monster(self, name: str ='chicken') -> None:
        print(f"Moving to the nearest {name} spot !")
        self.move_service.travel_to_nearest_object(name)

        while(True):
            self.fight_service.fight()

    def sell_object(self, code: str, quantity: int = 1) -> None:
        self.move_service.travel_to_nearest_object('grand_exchange')
        self.connexion.post(
            f"my/{self.model.character_name}/action/ge/sell",
            {
                "code": code,
                "quantity": quantity,
                "price": self.inventory.find_item(code).get_sell_price()
            }
        )

        return None

