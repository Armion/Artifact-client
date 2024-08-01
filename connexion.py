import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Connexion:
    def __init__(self, base_url = None, token = None):
        self.base_url = base_url or os.getenv('BASE_URL', 'https://api.artifactsmmo.com')
        self.token = token or os.getenv('TOKEN', None)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def print_request(self, prepared_request):
        print(f'URL: {prepared_request.url}')
        print(f'Method: {prepared_request.method}')
        print(f'Headers: {prepared_request.headers}')
        if prepared_request.body:
            print(f'Body: {prepared_request.body.decode("utf-8")}')

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.post(url, headers=self.headers, json=data)

        return self._handle_response(response)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            response.raise_for_status()