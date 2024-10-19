import os
import json
import requests
from endpoints.endpoint import Endpoint


class AuthorizeUser(Endpoint):
    CREDENTIALS_FILE = 'credentials.json'

    def get_token(self):
        self.token = self.__get_token_from_file()
        if self.token:
            if self.is_token_alive():
                return self.token
            else:
                self.token = self.__fetch_token_from_page()
        self.__save_token_to_file(self.token)
        return self.token

    def __get_token_from_file(self):
        if os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, 'r', encoding='utf-8') as file:
                credentials = json.load(file)
                return credentials.get("token")
        return None

    def __fetch_token_from_page(self):
        name = {"name": "sergey"}
        self.response = requests.post(self.url + 'authorize', json=name)

        if self.response.status_code == 200:
            return self.response.json()["token"]
        else:
            raise Exception("Failed to retrieve token: " + self.response.text)

    def __save_token_to_file(self, token):
        with open(self.CREDENTIALS_FILE, 'w', encoding='utf-8') as file:
            file.write(json.dumps({"token": token}, ensure_ascii=False))

    def is_token_alive(self):
        self.response = requests.get(f"{self.url}authorize/{self.token}")
        return True if self.response.status_code == 200 else False


test = AuthorizeUser()
print(test.get_token())
