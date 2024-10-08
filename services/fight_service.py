from tools.waitable import Waitable
from character.character_model import CharacterModel
from connexion import Connexion
from tools.server import Server

import dpath

class FightService(Waitable):
    def __init__(self, model: CharacterModel) -> None:
        self.model = model
        self.connexion = Connexion()
        self.server = Server()

    def fight(self, verbose: bool = True) -> None:
        self.wait_for_cd()
        print("starting the fight !")

        self.model.update_data(
            dpath.get(
                self.connexion.post(
                    f"my/{self.model.character_name}/action/fight"), 'data/character'
                )
        )

        if verbose == True:
            self.model.display_character()