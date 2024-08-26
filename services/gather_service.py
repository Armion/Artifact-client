from tools.waitable import Waitable
from character.character_model import CharacterModel
from connexion import Connexion
from tools.server import Server

import dpath

class GatherService(Waitable):
    def __init__(self, model: CharacterModel) -> None:
        self.model = model
        self.connexion = Connexion()
        self.server = Server()

    def gather(self):
        self.wait_for_cd()
        print("Starting gathering")

        self.model.update_data(
            dpath.util.get(
                self.connexion.post(f"my/{self.model.character_name}/action/gathering"), 'data/character'
            )
        )