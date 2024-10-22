import requests
import allure

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class GetOneMeme(Endpoint):

    @allure.step('Get a meme using GET method')
    def get_one_meme(self, meme_id):
        self.response = requests.get(
            f"{self.url}meme/{meme_id}",
            headers={"Authorization": self.token}
        )
        self.check_response(HTTPStatus.OK)

    @allure.step('Check for 404 status code when meme does not exist')
    def check_meme_not_found(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        self.check_response(HTTPStatus.NOT_FOUND)

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        for key in expected_keys:
            assert key in self.response.json(), f"Key '{key}' not found in response"

    @allure.step('Check unauthorized access')
    def check_unauthorized_access(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}")
        self.check_response(HTTPStatus.UNAUTHORIZED)

    @allure.step('Check that response is not empty')
    def check_response_not_empty(self):
        assert len(self.response.json()) > 0, "Response is empty"
