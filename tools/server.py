from datetime import datetime, timedelta
from connexion import Connexion
import dpath.util

class Server:
    def __init__(self) -> None:
        self.connexion = Connexion()
        self.delta = None
        self.__fetch_data__()

    def __fetch_data__(self) -> None:
        self.data = self.connexion.get('')
        self.__parse_date__()
        self.delta_time(sync=False)

    def get_server_time(self, sync: bool = True) -> datetime:
        if(sync):
            self.__fetch_data__()
        
        self.__parse_date__()
        return self.server_time

    def get_server_current_time(self, sync: bool = False) -> datetime:
        if (not sync):
            self.current_time = datetime.now() + self.delta_time(sync=False)
        else:
            self.current_time = datetime.now() + self.delta_time()
        return self.current_time

    def delta_time(self, sync = True) -> timedelta:
        if (not sync):
            if self.delta is None:
                self.delta = self.server_time - datetime.now()
            return self.delta
        
        self.delta = self.get_server_time() - datetime.now()
        return self.delta
    
    def __parse_date__(self) -> None:
        self.server_time = datetime.strptime(
            dpath.get(self.data, 'data/server_time'),
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        return None