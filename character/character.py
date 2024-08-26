from connexion import Connexion
from tools.server import Server
from map import Map
from services.move_service import MoveService
from character.character_model import CharacterModel

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

    def move(self, x: int, y: int) -> None:
        self.move_service.wait_for_cd()
        self.move_service.move_character(x, y)
        self.model.update_data()

    def gather(self):
        self.move_service.wait_for_cd()
        print("Starting gathering")

        self.model.update_data(
            dpath.util.get(
                self.connexion.post(f"my/{self.model.character_name}/action/gathering"), 'data/character'
            )
        )

    def fight(self, verbose: bool = True) -> None:
        self.move_service.wait_for_cd()
        print("starting the fight !")

        self.model.update_data(
            dpath.get(
                self.connexion.post(
                    f"my/{self.model.character_name}/action/fight"), 'data/character'
                )
        )
        
        if verbose == True:
            self.model.display_character()

    def wait_for_cd(self) -> None:
        remaining_seconds = (self.model.cooldown_expiration - self.server.get_server_current_time()).total_seconds() + 0.6

        if (remaining_seconds <= 0):
            print("No CD to wait for !")
            return None
        
        print(f"Waiting CD of {remaining_seconds} seconds")

        for _ in tqdm(range(int(remaining_seconds * 10)), desc="Cooldown Progress", unit="0.1s"):
            sleep(0.1)

        self.model.get_data()

    def farm_monster(self, name: str ='chicken') -> None:
        print(f"Moving to the nearest {name} spot !")
        self.move_service.travel_to_nearest_object(name)

        while(True):
            self.fight()

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

