from items.inventory import Inventory
from tools.colors import print_color, Color

from datetime import datetime
import requests
import dpath
from connexion import Connexion
from errors.exceptions import CharacterNotFoundError

class CharacterModel:
    def __init__(self,character_name: str, data: dict = None) -> None:
        self.character_name = character_name
        self.data = data
        self.connexion = Connexion()

    def update_data(self, data: dict = None) -> None:

        if data is None or data == {}:
            self.get_data()
        else:
            self.data = data
        
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
    
    def display_character(self, verbose: bool = False) -> None:
        print_color(f"lvl : {self.lvl}", Color.BLUE)
        print_color(f"hp : {self.hp}", Color.RED)
        print_color(f"xp to next lvl: {self.needed_xp}", Color.BLUE)
        print_color(f"gold : {self.gold}", Color.YELLOW)

        if(verbose):
            self.inventory.display()
            print(f"coordinates x: {self.pos_x} y: {self.pos_y}")