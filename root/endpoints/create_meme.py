import requests
import allure
from root.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step('Create a new meme with valid data')
    def create_a_meme(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        try:
            self.meme_id = self.response.json()['id']
            self.check_response_200()
        except requests.exceptions.JSONDecodeError as e:
            print(e)

    @allure.step('Create a new meme with invalid data')
    def create_a_meme_with_invalid_data(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response_400()

    @allure.step('Check parameter values in the new meme')
    def check_response_values(self, data):
        for key, value in data.items():
            assert str(self.response.json()[key]) == str(value), \
                f"Value of meme should be {self.response.json()[key]}, but it's: {value}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        for key in expected_keys:
            assert key in response_json, f"{key} not found in response"

    @allure.step('Check specific parameter value')
    def check_specific_parameter(self, key, expected_value):
        assert self.response.json()[key] == expected_value, \
            f"{key} is wrong: '{self.response.json()[key]}'"

    @allure.step('Check for errors with invalid data')
    def check_invalid_data(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response_200()

    @allure.step('Check for duplicate creation')
    def check_duplicate_creation(self, data):
        self.create_a_meme(data)
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response_200()

    @allure.step('Create a meme by unauthorized user')
    def create_meme_unauthorized(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data)
        self.check_response_401()
