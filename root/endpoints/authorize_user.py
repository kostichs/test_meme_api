import os
import json
import requests
import allure
from root.endpoints.endpoint import Endpoint


class AuthorizeUser(Endpoint):

    def __init__(self, credentials, username):
        super().__init__(username)
        self.credentials = credentials

    @allure.step('Check if the old token is still valid')
    def get_token(self):
        Endpoint.token = self.__get_token_from_file()

    @allure.step('Getting a new token')
    def get_new_token(self):
        self.token = self.__load_token_from_page()
        self.__save_token_to_file(self.token)

    @allure.step('Check if there is a saved valid token in a file')
    def __get_token_from_file(self):
        if os.path.exists(self.credentials):
            with open(self.credentials, 'r', encoding='utf-8') as file:
                credentials = json.load(file)
                return credentials.get("token")
        return self.get_new_token()

    def __load_token_from_page(self):
        name = {"name": self.username}
        self.response = requests.post(self.url + 'authorize', json=name)
        if self.response.status_code == 200:
            return self.response.json()["token"]
        else:
            raise Exception("Failed to get token: " + self.response.text)

    def __save_token_to_file(self, token):
        with open(self.credentials, 'w', encoding='utf-8') as file:
            json.dump({"token": token}, file, ensure_ascii=False)

    @allure.step('Check if token is valid')
    def check_token(self):
        assert "token" in self.response.json(), "Token is missing in the response"

    @allure.step('Check Username matching')
    def check_username(self):
        assert self.response.json()['user'] == self.username, f"Username is wrong: {self.response.json()['user']}"
