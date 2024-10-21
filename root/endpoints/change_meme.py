import allure
import requests
from root.endpoints.endpoint import Endpoint


class FullChangeMeme(Endpoint):

    @allure.step('Change meme with PUT method')
    def change_meme(self, data, meme_id):
        data['id'] = meme_id
        self.response = requests.put(
            f"{self.url}meme/{meme_id}",
            json=data,
            headers={"Authorization": self.token}
        )
        try:
            self.meme_id = self.response.json()['id']
            self.check_response_200()
        except requests.exceptions.JSONDecodeError:
            print("JSONDecodeError")

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
        self.check_response_400()

    @allure.step('Change meme by unauthorized user')
    def change_meme_unauthorized(self, data, meme_id):
        self.response = requests.put(f"{self.url}/meme/{meme_id}", json=data)
        self.check_response_401()

    @allure.step('Check the name of user who changed the meme')
    def check_changer_name(self):
        assert self.response.json()['updated_by'] == self.USERNAME, \
            f"Name of user updated the meme is wrong: {self.response.json()['updated_by']}"
