import requests
import allure

from root.data.htttp_enum import HTTPStatus
from root.endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete an object using DELETE method')
    def delete_meme(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        self.check_response(HTTPStatus.OK)

    @allure.step('Check response 404: Re-deletion, Non-existing meme, invalid id')
    def check_negative_deletion(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        self.check_response(HTTPStatus.NOT_FOUND)

    @allure.step('Attempt to delete a meme without authorization')
    def delete_meme_unauthorized(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}")
        self.check_response(HTTPStatus.UNAUTHORIZED)
