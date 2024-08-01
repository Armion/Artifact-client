import json
from connexion import Connexion

class Map:
    def __init__(self, source = "local"):
        if source == "local":
            self.local_load()
        else:
            self.online_load()
    
    def local_load(self):
        with open('data/map.json', 'r') as file:
            self.data = json.load(file)
    
    def online_load(self):
        self.connexion = Connexion()