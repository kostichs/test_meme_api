import requests

from root.endpoints.endpoint import Endpoint


class GetAllMemes(Endpoint):

    def get_all_memes(self):
        self.response = requests.get(
            f"{self.url}/meme",
            headers={"Authorization": self.token}
        )
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"
