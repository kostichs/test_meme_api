import requests
import allure
from root.endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    def __init__(self, token):
        super().__init__()
        self.token = token

    @allure.step('Delete an object by id using DELETE method')
    def delete_meme(self, meme_id, authorized=True):
        if authorized:
            headers = {"Authorization": self.token}
        else:
            headers = None
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers=headers)
