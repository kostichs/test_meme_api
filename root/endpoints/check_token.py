import requests
from root.endpoints.endpoint import Endpoint


class CheckExistingToken(Endpoint):

    def is_token_alive(self, token):
        if not token:
            return False

        self.response = requests.get(f"{self.url}authorize/{token}")
        return self.response.status_code == 200