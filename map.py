import json
import math
from connexion import Connexion
from tools.data_handler import DataHandler

class Map(DataHandler):
    def __init__(self, source = "offline"):
        if source == "offline":
            self.offline_load('data/map.json')
        else:
            self.online_load('maps')

    def find_object(self, name):
        return [map for map in self.data['data'] if map['content'] is not None and map['content'].get('code') == name]

    def find_nearest_object(self, pos_x, pos_y, name):
        return self.nearest_map(pos_x, pos_y, self.find_object(name))

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