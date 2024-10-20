import requests
import allure
from root.endpoints.endpoint import Endpoint


class GetOneMeme(Endpoint):

    @allure.step('Get a meme using GET method')
    def get_one_meme(self, meme_id):
        self.response = requests.get(
            f"{self.url}meme/{meme_id}",
            headers={"Authorization": self.token}
        )

    @allure.step('Check for 404 status code when meme does not exist')
    def check_meme_not_found(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        assert self.response.status_code == 404, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        for key in expected_keys:
            assert key in response_json, f"Key '{key}' not found in response"

    @allure.step('Check unauthorized access')
    def check_unauthorized_access(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}")
        assert self.response.status_code == 401, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check that response is not empty')
    def check_response_not_empty(self):
        response_json = self.response.json()
        assert response_json, "Response is empty"
