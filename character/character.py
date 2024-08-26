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

    def move(self, x: int, y: int) -> None:
        self.wait_for_cd()
        MoveService(self.character_name).move_character(x, y)
        self.model.update_data()

    def gather(self):
        self.wait_for_cd()
        print("Starting gathering")

        self.model.update_data(
            dpath.util.get(
                self.connexion.post(f"my/{self.model.character_name}/action/gathering"), 'data/character'
            )
        )

    def fight(self, verbose: bool = True) -> None:
        self.wait_for_cd()
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
        self.travel_to_nearest_object(name)

        while(True):
            self.fight()

    def sell_object(self, code: str, quantity: int = 1) -> None:
        self.travel_to_nearest_object('grand_exchange')
        self.connexion.post(
            f"my/{self.character_name}/action/ge/sell",
            {
                "code": code,
                "quantity": quantity,
                "price": self.inventory.find_item(code).get_sell_price()
            }
        )

        return None



    def travel_to_nearest_object(self, name: str, online: bool = False) -> None:
        map = Map('online') if online else Map('offline')
        nearest = map.find_nearest_object(self.model.pos_x, self.model.pos_y, name)

        if self.model.pos_x == nearest['x'] and self.model.pos_y == nearest['y']:
            print("You are already there !")
            self.model.update_data()
            return None
        else:
            self.wait_for_cd()
            self.move(nearest['x'], nearest['y'])
        return None

