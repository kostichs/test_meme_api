import requests
import allure

from root.endpoints.endpoint import Endpoint


class GetAllMemes(Endpoint):
    @allure.step('Getting all memes using GET method')
    def get_all_memes(self):
        self.response = requests.get(
            f"{self.url}/meme",
            headers={"Authorization": self.token}
        )
        self.check_response_200()

    @allure.step('Check response structure for all memes')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        assert 'data' in response_json, "Response does not contain 'data' key"
        assert isinstance(response_json['data'], list), "Data is not a list"
        for meme in response_json['data']:
            for key in expected_keys:
                assert key in meme, f"Key '{key}' not found in meme: {meme}"

    @allure.step('Check values in memes')
    def check_meme_values(self, expected_data):
        response_json = self.response.json()
        for meme in response_json:
            for key, expected_value in expected_data.items():
                assert meme[key] == expected_value, f"Value of '{key}' is wrong in meme {meme['id']}: '{meme[key]}'"

    @allure.step('Check if response is not empty')
    def check_response_not_empty(self):
        response_json = self.response.json()
        assert len(response_json['data']) > 0, "Response is empty"

    @allure.step('Check for unauthorized access')
    def check_unauthorized_access(self):
        self.response = requests.get(f"{self.url}/meme")
        self.check_response_401()

    @allure.step('Check for invalid URL')
    def check_invalid_url(self, data):
        self.response = requests.get(f"{self.url}{data}", headers={"Authorization": self.token})
        self.check_response_404()
