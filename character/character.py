from connexion import Connexion
from errors.exceptions import CharacterNotFoundError
from tools.colors import print_color, Color
from tools.server import Server
from map import Map
from items.inventory import Inventory

import dpath
from time import sleep
from tqdm import tqdm
import requests
from datetime import datetime, timedelta

class Character:
    def __init__(self, character_name):
        self.character_name = character_name
        self.connexion = Connexion()
        self.server = Server()
        self.update_data()

    def move(self, x: int, y: int) -> None:
        self.wait_for_cd()
        self.connexion.post(
            f"my/{self.character_name}/action/move",
                {
                    "x": x,
                    "y": y
                }
            )
        self.update_data()

    def get_data(self) -> None:
        try:
            response = self.connexion.get(f"characters/{self.character_name}")
            self.data = dpath.get(response, 'data')
            self.inventory = Inventory(self.data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise CharacterNotFoundError(self.character_name)
            else:
                raise e

    def update_data(self, fetch : bool = True) -> None:
        if fetch == True:
            self.get_data()
        
        self.hp = self.data['hp']
        self.lvl = self.data['level']
        self.gold = self.data['gold']
        self.current_xp = self.data['xp']
        self.next_lvl_xp = self.data['max_xp']
        self.needed_xp = self.next_lvl_xp - self.current_xp
        self.cooldown = self.data['cooldown']
        self.cooldown_expiration = datetime.strptime(
            self.data['cooldown_expiration'],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.pos_x = self.data['x']
        self.pos_y = self.data['y']

    def gather(self):
        self.wait_for_cd()
        print("Starting gathering")
        self.data = dpath.util.get(self.connexion.post(f"my/{self.character_name}/action/gathering"), 'data/character')
        self.update_data(False)

    def fight(self, verbose: bool = True) -> None:
        self.wait_for_cd()
        print("starting the fight !")
        self.data = dpath.get(self.connexion.post(f"my/{self.character_name}/action/fight"), 'data/character')
        self.update_data(False)
        
        if verbose == True:
            self.display_character()

    def display_character(self, verbose: bool = False) -> None:
        print_color(f"lvl : {self.lvl}", Color.BLUE)
        print_color(f"hp : {self.hp}", Color.RED)
        print_color(f"xp to next lvl: {self.needed_xp}", Color.BLUE)
        print_color(f"gold : {self.gold}", Color.YELLOW)

        if(verbose):
            self.inventory.display()
            print(f"coordinates x: {self.pos_x} y: {self.pos_y}")

    def wait_for_cd(self) -> None:
        remaining_seconds = (self.cooldown_expiration - self.server.get_server_current_time()).total_seconds() + 0.5

        if (remaining_seconds <= 0):
            print("No CD to wait for !")
            return None
        
        print(f"Waiting CD of {remaining_seconds} seconds")

        for _ in tqdm(range(int(remaining_seconds * 10)), desc="Cooldown Progress", unit="0.1s"):
            sleep(0.1)

        self.get_data()

    def farm_monster(self, name: str ='chicken') -> None:
        print(f"Moving to the nearest {name} spot !")
        self.travel_to_nearest_object(name)

        while(True):
            self.fight()

    def travel_to_nearest_object(self, name: str, online: bool = False) -> None:
        map = Map('online') if online else Map('offline')
        nearest = map.find_nearest_object(self.pos_x, self.pos_y, name)

        if self.pos_x == nearest['x'] and self.pos_y == nearest['y']:
            print("You are already there !")
            self.update_data()
            return None
        else:
            self.wait_for_cd()
            self.move(nearest['x'], nearest['y'])
        return None

