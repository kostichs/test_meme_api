import requests
import allure

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    def __init__(self):
        self.meme_id = None
        self.duplicate_id = None

    @allure.step('Create a new meme with valid data')
    def create_a_meme(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        if self.response.status_code == HTTPStatus.OK.value:
            try:
                self.meme_id = self.response.json().get('id')
                if not self.meme_id:
                    raise ValueError("Meme ID not found in the response.")
            except Exception as e:
                print(f"Failed to parse meme ID: {str(e)}")
                raise
        else:
            print(
                f"Failed to create meme. Status code: {self.response.status_code}, Response: {self.response.text}")
            raise Exception(f"Unexpected status code: {self.response.status_code}")
        self.check_response(HTTPStatus.OK)

    @allure.step('Create a new meme with invalid data')
    def create_a_meme_with_invalid_data(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response(HTTPStatus.BAD_REQUEST)

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
        self.check_response(HTTPStatus.OK)

    @allure.step('Check for duplicate creation')
    def check_duplicate_creation(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response(HTTPStatus.OK)
        # There is a duplicate meme, so it will be deleted separately by duplicate_id
        self.duplicate_id = self.response.json()['id']

    @allure.step('Create a meme by unauthorized user')
    def create_meme_unauthorized(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data)
        self.check_response(HTTPStatus.UNAUTHORIZED)
