import requests
import allure

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class GetAllMemes(Endpoint):

    def __init__(self, token):
        super().__init__()
        self.token = token

    @allure.step('Getting all memes using GET method')
    def get_all_memes(self, authorized=True):
        if authorized:
            headers = {"Authorization": self.token}
        else:
            headers = None

        self.response = requests.get(
            f"{self.url}/meme",
            headers=headers
        )

    @allure.step('Check response structure for all memes')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        assert 'data' in response_json, "Response does not contain 'data' key"
        assert isinstance(response_json['data'], list), "Data is not a list"
        for meme in response_json['data']:
            for key in expected_keys:
                assert key in meme, f"Key '{key}' not found in meme: {meme}"

    @allure.step('Check if response is not empty')
    def check_response_not_empty(self):
        assert len(self.response.json()['data']) > 0, "Response is empty"

    @allure.step('Check for unauthorized access')
    def check_unauthorized_access(self):
        self.response = requests.get(f"{self.url}/meme")


    @allure.step('Check for invalid URL')
    def check_invalid_url(self, data):
        self.response = requests.get(f"{self.url}{data}", headers={"Authorization": self.token})
        self.check_response(HTTPStatus.NOT_FOUND)
