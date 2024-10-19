import requests
from root.endpoints.endpoint import Endpoint


class GetOneMeme(Endpoint):

    def get_one_meme(self, meme_id):
        self.response = requests.get(
            f"{self.url}/meme/{meme_id}",
            headers={"Authorization": self.token}
        )
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"
