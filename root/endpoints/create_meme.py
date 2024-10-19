import requests
from root.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    def create_a_meme(self, data):
        self.response = requests.post(
            f"{self.url}/meme",
            json=data,
            headers={"Authorization": self.token}
        )
        print("Create meme:", self.response.status_code)
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"
