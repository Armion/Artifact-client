from connexion import Connexion
from map import Map
from character.character_model import CharacterModel
from tools.waitable import Waitable
from tools.server import Server

class MoveService(Waitable):
    def __init__(self, model: CharacterModel) -> None:
        self.model = model
        self.connexion = Connexion()
        self.server = Server()
    
    def move_character(self, x: int, y: int) -> None:
        self.connexion.post(
            f"my/{self.model.character_name}/action/move",
                {
                    "x": x,
                    "y": y
                }
        )
        self.model.update_data()

    def travel_to_nearest_object(self, name: str, online: bool = False) -> None:
        map = Map('online') if online else Map('offline')
        nearest = map.find_nearest_object(self.model.pos_x, self.model.pos_y, name)

        if self.model.pos_x == nearest['x'] and self.model.pos_y == nearest['y']:
            print("You are already there !")
            self.model.update_data()
            return None
        else:
            self.wait_for_cd()
            self.move_character(nearest['x'], nearest['y'])
        return None
