import requests
from root.endpoints.endpoint import Endpoint


class CheckExistingToken(Endpoint):

    def is_token_alive(self):
        self.response = requests.get(f"{self.url}authorize/{self.token}")
        if self.response.status_code == 200:
            return True
        else:
            return False
