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
            self.response_json = self.response.json()
            self.meme_id.append(self.response.json()['id'])
        except requests.exceptions.JSONDecodeError:
            self.response_json = ""

    @allure.step('Check parameter values in the updated meme')
    def check_response_values(self, data):
        for key, value in data.items():
            assert str(self.response.json()[key]) == str(
                value), f"Parameter {key} with {self.response.json()[key]} value is wrong: {value}"

    @allure.step('Check response structure')
    def check_response_structure(self, expected_keys):
        response_json = self.response.json()
        for key in expected_keys:
            assert key in response_json, f"Parameter '{key}' not found in response"

    @allure.step('Check specific parameter value')
    def check_specific_parameter(self, key, expected_value):
        assert self.response.json()[key] == expected_value, \
            f"Parameter '{key}' is not '{self.response.json()[key]}'"

    @allure.step('Check for errors with invalid data')
    def check_invalid_data(self, data, meme_id):
        self.response = requests.put(
            f"{self.url}meme/{meme_id}",
            json=data,
            headers={"Authorization": self.token}
        )
        self.check_response_404()

    @allure.step('Check for required parameters')
    def check_missing_required_parameters(self, missing_params, meme_id):
        for param in missing_params:
            data = {k: v for k, v in self.response_json.items() if k != param}
            response = requests.put(
                f"{self.url}meme/{meme_id}",
                json=data,
                headers={"Authorization": self.token}
            )
            self.check_response_404()

    @allure.step('Change meme by unauthorized user')
    def change_meme_unauthorized(self, data):
        self.response = requests.put(f"{self.url}/meme/{self.get_meme_id}", json=data)
        self.check_response_401()
