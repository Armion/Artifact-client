from connexion import Connexion
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

    def wait_for_cd(self):
        time.sleep(float(self.cooldown) + 0.5)
        self.get_data()

    def farm_chicken(self):
        self.wait_for_cd()

