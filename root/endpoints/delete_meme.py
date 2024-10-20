import requests
import allure
from root.endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete an object using DELETE method')
    def delete_meme(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        try:
            self.meme_id.append(self.response.json().get('id', ''))
        except requests.exceptions.JSONDecodeError:
            self.meme_id = ""

    @allure.step('Check response 404: Re-deletion, Non-existing meme, invalid id')
    def check_negative_deletion(self, meme_id):
        self.response = requests.get(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        self.check_response_404()

    @allure.step('Attempt to delete a meme without authorization')
    def delete_meme_unauthorized(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}")
        self.check_response_401()
