import requests
import allure
from root.endpoints.endpoint import Endpoint


class GetOneMeme(Endpoint):

    def __init__(self, token):
        super().__init__()
        self.token = token

    @allure.step('Get a meme using GET method')
    def get_meme_by_id(self, meme_id, authorized=True):
        if authorized:
            headers = {"Authorization": self.token}
        else:
            headers = None
        self.response = requests.get(
            f"{self.url}meme/{meme_id}",
            headers=headers
        )

    @allure.step('Check if id of received meme is equal the given id')
    def check_id(self, meme_id):
        assert self.response.json()['id'] == meme_id, f"Receive ID is wrong: {self.response.json()['id']}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        for key in expected_keys:
            assert key in self.response.json(), f"Key '{key}' not found in response"

    @allure.step('Check that response is not empty')
    def check_response_not_empty(self):
        assert len(self.response.json()) > 0, "Response is empty"
