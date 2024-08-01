from connexion import Connexion
from map import Map
import dpath.util
import time

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
        self.data = dpath.util.get(self.connexion.get(f"characters/{self.character_name}"), 'data')

    def update_data(self):
        self.get_data()
        self.hp = self.data['hp']
        self.lvl = self.data['level']
        self.gold = self.data['gold']
        self.current_xp = self.data['total_xp']
        self.next_lvl_xp = self.data['max_xp']
        self.cooldown = self.data['cooldown']
        self.pos_x = self.data['x']
        self.pos_y = self.data['y']

    def fight(self, verbose = True):
        self.wait_for_cd()
        self.connexion.post(f"my/{self.character_name}/action/fight")
        if verbose == True:
            self.update_data()
            self.display_character()

    def display_character(self):
        print(f" lvl : {self.lvl}")
        print(f"hp : {self.hp}")
        print(f"xp to next lvl: {self.next_lvl_xp}")
        print(f"coordinates x: {self.pos_x} y: {self.pos_y}")
        print(f"gold : {self.gold}")

    def wait_for_cd(self):
        time.sleep(float(self.cooldown) + 0.5)
        self.get_data()

    def farm_chicken(self):
        self.wait_for_cd()
        print("Moving to the nearest chickens spot !")
        self.travel_to_nearest_monster('chicken')

        while(True):
            self.fight()

    def travel_to_nearest_monster(self, name, online = False):
        map = Map('online') if online else Map('offline')
        nearest = map.find_nearest_monster(self.pos_x, self.pos_y, name)
        self.wait_for_cd()

        if self.pos_x == nearest['x'] and self.pos_y == nearest['y']:
            print("You are already there !")
            return None
        else:
            self.move(nearest['x'], nearest['y'])
        return None

