import requests
from root.endpoints.endpoint import Endpoint


class FullChangeMeme(Endpoint):

    def change_meme(self, data, meme_id):
        data['id'] = meme_id
        self.response = requests.put(
            f"{self.url}/meme/{meme_id}",
            json=data,
            headers={"Authorization": self.token}
        )
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"