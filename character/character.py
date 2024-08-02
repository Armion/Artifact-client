from connexion import Connexion
from errors.exceptions import CharacterNotFoundError
from map import Map
from items.inventory import Inventory

import dpath.util
from time import sleep
from tqdm import tqdm
import requests

class Character:
    def __init__(self, character_name):
        self.character_name = character_name
        self.connexion = Connexion()
        self.update_data()

    def move(self, x, y):
        self.connexion.post(
            f"my/{self.character_name}/action/move",
                {
                    "x": x,
                    "y": y
                }
            )
        self.update_data()

    def get_data(self):
        try:
            response = self.connexion.get(f"characters/{self.character_name}")
            self.data = dpath.util.get(response, 'data')
            self.inventory = Inventory(self.data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise CharacterNotFoundError(self.character_name)
            else:
                raise e

    def update_data(self, fetch = True):
        if fetch == True:
            self.get_data()
        
        self.hp = self.data['hp']
        self.lvl = self.data['level']
        self.gold = self.data['gold']
        self.current_xp = self.data['xp']
        self.next_lvl_xp = self.data['max_xp']
        self.needed_xp = self.next_lvl_xp - self.current_xp
        self.cooldown = self.data['cooldown']
        self.pos_x = self.data['x']
        self.pos_y = self.data['y']

    def fight(self, verbose = True):
        self.wait_for_cd()
        print("starting the fight !")
        self.data = dpath.util.get(self.connexion.post(f"my/{self.character_name}/action/fight"), 'data/character')
        self.update_data(False)
        
        if verbose == True:
            self.display_character()

    def display_character(self):
        print(f" lvl : {self.lvl}")
        print(f"hp : {self.hp}")
        print(f"xp to next lvl: {self.needed_xp}")
        print(f"coordinates x: {self.pos_x} y: {self.pos_y}")
        print(f"gold : {self.gold}")

    def wait_for_cd(self):
        total_time = float(self.cooldown) + 0.5
        print(f"Waiting CD of {total_time} seconds")

        for _ in tqdm(range(int(total_time * 10)), desc="Cooldown Progress", unit="0.1s"):
            sleep(0.1)

        self.get_data()

    def farm_monster(self, name='chicken'):
        print(f"Moving to the nearest {name} spot !")
        self.travel_to_nearest_object(name)

        while(True):
            self.fight()

    def travel_to_nearest_object(self, name, online = False):
        map = Map('online') if online else Map('offline')
        nearest = map.find_nearest_object(self.pos_x, self.pos_y, name)
        self.wait_for_cd()

        if self.pos_x == nearest['x'] and self.pos_y == nearest['y']:
            print("You are already there !")
            self.update_data()
            return None
        else:
            self.move(nearest['x'], nearest['y'])
        return None

