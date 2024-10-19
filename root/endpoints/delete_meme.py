import requests
import allure
from root.endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete an object using DELETE method')
    def delete_meme(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})

    @allure.step("Check successful deletion")
    def check_success(self):
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check the re-deletion of the deleted meme')
    def check_meme_deleted(self, meme_id):
        response = requests.get(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        assert response.status_code == 404, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Attempt to delete a non-existing meme')
    def delete_non_existing_meme(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        assert self.response.status_code == 404, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Attempt to delete a meme with invalid ID format')
    def delete_meme_with_invalid_id(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}", headers={"Authorization": self.token})
        assert self.response.status_code == 404, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Attempt to delete a meme without authorization')
    def delete_meme_without_auth(self, meme_id):
        self.response = requests.delete(f"{self.url}meme/{meme_id}")
        assert self.response.status_code == 401, f"Unexpected status code: {self.response.status_code}"
