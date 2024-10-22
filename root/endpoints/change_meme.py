import allure
import requests

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class FullChangeMeme(Endpoint):

    def __init__(self, username):
        super().__init__(username=username)

    @allure.step('Change meme with PUT method')
    def change_meme(self, data, meme_id):
        data['id'] = meme_id
        self.response = requests.put(
            f"{self.url}meme/{meme_id}",
            json=data,
            headers={"Authorization": self.token}
        )
        self.check_response(HTTPStatus.OK)

    @allure.step('Check parameter values in the updated meme')
    def check_response_values(self, data):
        for key, value in data.items():
            assert str(self.response.json()[key]) == str(
                value), f"Parameter {key} with {self.response.json()[key]} value is wrong: {value}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        for key in expected_keys:
            assert key in self.response.json(), f"Parameter '{key}' not found in response"

    @allure.step('Check for errors with invalid data')
    def check_invalid_data(self, data, meme_id):
        self.response = requests.put(
            f"{self.url}meme/{meme_id}",
            json=data,
            headers={"Authorization": self.token}
        )
        self.check_response(HTTPStatus.BAD_REQUEST)

    @allure.step('Change meme by unauthorized user')
    def change_meme_unauthorized(self, data, meme_id):
        self.response = requests.put(f"{self.url}/meme/{meme_id}", json=data)
        self.check_response(HTTPStatus.UNAUTHORIZED)

    @allure.step('Check the name of user who changed the meme')
    def check_changer_name(self):
        assert self.response.json()['updated_by'] == self.username, \
            f"Name of user who updated meme is wrong: {self.response.json()['updated_by']}"
