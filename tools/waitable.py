from tqdm import tqdm
from time import sleep




class Waitable:
    def __init__(self) -> None:
        pass

    def wait_for_cd(self) -> None:
        remaining_seconds = (self.model.cooldown_expiration - self.server.get_server_current_time()).total_seconds() + 0.6

        if (remaining_seconds <= 0):
            print("No CD to wait for !")
            return None
        
        print(f"Waiting CD of {remaining_seconds} seconds")

        for _ in tqdm(range(int(remaining_seconds * 10)), desc="Cooldown Progress", unit="0.1s"):
            sleep(0.1)

        self.model.get_data()