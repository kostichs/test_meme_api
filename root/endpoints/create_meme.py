import requests
import allure
from root.endpoints.endpoint import Endpoint

class CreateMeme(Endpoint):
    @allure.step('Create a new object with POST method')
    def create_a_meme(self, data=None, headers=None):
        headers = headers if headers else {"Authorization": self.token}
        data = data if data else self.default_data
        self.response = requests.post(f"{self.url}/meme", json=data, headers=headers)
        try:
            self.response_json = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.response_json = ""


    @allure.step('Check parameter values in the new meme')
    def check_response_values(self, data):
        for parameter_key, parameter_value in data.items():
            assert self.response.json()[parameter_key] == parameter_value, \
                f"Value of the created meme is wrong: {parameter_value}"

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
        assert self.response.status_code != 200, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check for required parameters')
    def check_missing_required_parameters(self, missing_params):
        for param in missing_params:
            data = {k: v for k, v in self.default_data.items() if k != param}
            response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
            assert response.status_code == 400, f"Unexpected status code: {response.status_code}"

    @allure.step('Check for duplicate creation')
    def check_duplicate_creation(self, data):
        self.create_a_meme(data)
        response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @allure.step('Create a meme by unauthorized user')
    def create_meme_with_unauthorized_user(self, data):
        response = requests.post(f"{self.url}/meme", json=data)
        assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
