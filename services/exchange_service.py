from tools.waitable import Waitable
from character.character_model import CharacterModel
from connexion import Connexion
from tools.server import Server

import dpath

class ExchangeService(Waitable):
    def __init__(self, model: CharacterModel) -> None:
        self.model = model
        self.connexion = Connexion()
        self.server = Server()

    def sell_object(self, code: str, quantity: int = 1) -> None:
        self.connexion.post(
            f"my/{self.model.character_name}/action/ge/sell",
            {
                "code": code,
                "quantity": quantity,
                "price": self.inventory.find_item(code).get_sell_price()
            }
        )

        return None