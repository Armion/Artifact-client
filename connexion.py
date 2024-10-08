import requests
from dotenv import load_dotenv
import os
from errors.exceptions import *

load_dotenv()

class Connexion:
    status_code_exceptions = {
        499: CooldownNotReady,
        498: CharacterNotFoundError,
        497: InventoryFull,
        486: CharacterLocked,
        502: ServerUnavailable,
        503: ServerUnavailable
    }

    def __init__(self, base_url: str = None, token: str = None) -> None:
        self.base_url = base_url or os.getenv('BASE_URL', 'https://api.artifactsmmo.com')
        self.token = token or os.getenv('TOKEN', None)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def print_request(self, prepared_request: str) -> None:
        print(f'URL: {prepared_request.url}')
        print(f'Method: {prepared_request.method}')
        print(f'Headers: {prepared_request.headers}')
        if prepared_request.body:
            print(f'Body: {prepared_request.body.decode("utf-8")}')

    def get(self, endpoint: str, params: hash =None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: hash=None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.post(url, headers=self.headers, json=data)

        return self._handle_response(response)

    def put(self, endpoint: str, data: hash =None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> requests.Response:
        if 200 <= response.status_code < 300:
            return response.json()
        elif response.status_code in self.status_code_exceptions:
            exception_class = self.status_code_exceptions[response.status_code]
            if exception_class == CharacterNotFoundError:
                raise exception_class(f"Character '{self.token}' not found.")
            raise exception_class()
        else:
            response.raise_for_status()