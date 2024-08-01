import json
import math
from connexion import Connexion

class Map:
    def __init__(self, source = "offline"):
        if source == "offline":
            self.offline_load()
        else:
            self.online_load()
    
    def offline_load(self):
        with open('data/map.json', 'r') as file:
            self.data = json.load(file)
    
    def online_load(self):
        self.connexion = Connexion()

        self.data = self.connexion.get('maps', { 'page' : 1, 'size': 100 })

        for i in range(2, self.data['pages'] + 1):
            self.data['data'].extend(
                self.connexion.get('maps', { 'page' : i, 'size': 100 })['data']
            )

    def save_data(self):
        with open('data/map.json', 'w', encoding= 'utf-8') as file:
            json.dump(self.data, file, indent=4)

    def find_monsters(self, name):
        return [map for map in self.data['data'] if map['content'] is not None and map['content'].get('code') == name]

    def find_nearest_monster(self, pos_x, pos_y, name):
        return self.nearest_map(pos_x, pos_y, self.find_monsters(name))

    def nearest_map(self, pos_x, pos_y, maps):
        nearest = None
        mindist = 0.0

        for map in maps:
            dist = self.distance(pos_x, pos_y, map['x'], map['y'])
            if nearest == None or dist < mindist :
                nearest = map
                mindist = dist
        
        return nearest

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)