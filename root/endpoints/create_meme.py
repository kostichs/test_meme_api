from multiprocessing.managers import Value

import requests
import allure

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.meme_id = None
        self.duplicate_id = None

    @allure.step('Create a new meme with valid data')
    def create_a_meme(self, data, authorized=True):
        if authorized:
            headers = {"Authorization": self.token}
        else:
            headers = None
        self.response = requests.post(f"{self.url}/meme", json=data, headers=headers)
        try:
            self.meme_id = self.response.json()['id']
        except ValueError:
            self.meme_id = ""

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

    @allure.step('Check for duplicate creation')
    def check_duplicate_creation(self, data):
        self.response = requests.post(f"{self.url}/meme", json=data, headers={"Authorization": self.token})
        self.check_response(HTTPStatus.OK)
        # There is a duplicate meme, so it will be deleted separately by duplicate_id
        self.duplicate_id = self.response.json()['id']
