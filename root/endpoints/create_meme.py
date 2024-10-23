import requests
import allure
from root.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.meme_id = None
        self.data = None

    @allure.step('Create a new meme with valid data')
    def create_a_meme(self, data, authorized=True):
        self.data = data
        if authorized:
            headers = {"Authorization": self.token}
        else:
            headers = None
        self.response = requests.post(f"{self.url}/meme", json=self.data, headers=headers)
        try:
            self.meme_id = self.response.json()['id']
        except ValueError:
            self.meme_id = ""

    @allure.step('Check parameter values in the new meme')
    def check_response_values(self):
        for key, value in self.data.items():
            assert str(self.response.json()[key]) == str(value), \
                f"Value of meme should be {self.response.json()[key]}, but it's: {value}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        for key in expected_keys:
            assert key in response_json, f"{key} not found in response"
