import os
import json
import requests
from root.endpoints.endpoint import Endpoint
import allure

class AuthorizeUser(Endpoint):
    CREDENTIALS_FILE = 'credentials.json'
    USERNAME = 'sergey'

    def get_old_token(self):
        self.token = self.__get_token_from_file()
        if self.token:
            return self.token

    def get_new_token(self):
        self.token = self.__fetch_token_from_page()
        self.__save_token_to_file(self.token)
        return self.token

    def __get_token_from_file(self):
        if os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, 'r', encoding='utf-8') as file:
                credentials = json.load(file)
                return credentials.get("token")
        return self.get_new_token()

    def __fetch_token_from_page(self):
        name = {"name": self.USERNAME}
        self.response = requests.post(self.url + 'authorize', json=name)

        if self.response.status_code == 200:
            return self.response.json()["token"]
        else:
            raise Exception("Failed to get token: " + self.response.text)

    def __save_token_to_file(self, token):
        with open(self.CREDENTIALS_FILE, 'w', encoding='utf-8') as file:
            json.dump({"token": token}, file, ensure_ascii=False)

    @allure.step('Check if token is valid')
    def check_token(self):
        assert "token" in self.response.json(), "Token is missing in the response"

    @allure.step('Check Username matching')
    def check_username(self):
        assert self.response.json()['user'] == self.USERNAME, f"Username is wrong: {self.response.json()['user']}"
