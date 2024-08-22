from datetime import datetime, timedelta
from connexion import Connexion
import dpath.util

class Server:
    def __init__(self) -> None:
        self.connexion = Connexion()
        self.__fetch_data__()

    def __fetch_data__(self) -> None:
        self.data = self.connexion.get('')

    def get_server_time(self) -> datetime:
        self.__fetch_data__()
        self.server_time = datetime.strptime(
            dpath.get(self.data, 'data/server_time'),
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        return self.server_time

    def delta_time(self, sync = True) -> timedelta:
        if (not sync and self.delta is not None):
            return self.delta
        
        self.delta = self.get_server_time() - datetime.now()
        return self.delta