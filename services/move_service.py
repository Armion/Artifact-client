from connexion import Connexion
from map import Map

class MoveService:
    def __init__(self, character_name: str) -> None:
        self.character_name = character_name
        self.connexion = Connexion()
    
    def move_character(self, x: int, y: int) -> None:
        self.connexion.post(
            f"my/{self.character_name}/action/move",
                {
                    "x": x,
                    "y": y
                }
        )

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
