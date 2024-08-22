import json
from connexion import Connexion

class DataHandler:
    def offline_load(self, filename: str) -> None:
        with open(filename, 'r') as file:
            self.data = json.load(file)

    def online_load(self, endpoint: str) -> None:
        self.connexion = Connexion()

        self.data = self.connexion.get(endpoint, { 'page' : 1, 'size': 100 })

        for i in range(2, self.data['pages'] + 1):
            self.data['data'].extend(
                self.connexion.get(endpoint, { 'page' : i, 'size': 100 })['data']
            )

    def save_data(self, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)