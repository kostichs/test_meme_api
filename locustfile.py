import random
from locust import task, HttpUser
from root.endpoints.authorize_user import AuthorizeUser
from root.data.test_parameters import MEME_DATA_POSITIVE, MEME_DATA_NEGATIVE


class ObjectUser(HttpUser):
    token = None
    headers = None
    meme_id = []

    def on_start(self):
        authorized_user = AuthorizeUser()
        self.token = authorized_user.get_token()
        self.headers = {"Authorization": self.token}

    @task(2)
    def get_all_memes(self):
        self.client.get(
            '/meme',
            headers=self.headers
        )

    @task(4)
    def get_one_meme(self):

        if self.meme_id:
            meme_id = random.choice(self.meme_id)
            self.client.get(
                f'/meme/{meme_id}',
                headers=self.headers
            )

    @task(5)
    def create_meme(self):
        data = random.choice(MEME_DATA_POSITIVE)
        response = self.client.post(
            '/meme',
            json=data,
            headers=self.headers
        )
        if response.status_code == 200:
            response_data = response.json()
            self.meme_id.append(response_data["id"])

    @task(1)
    def create_meme_with_negative_data(self):
        data = random.choice(MEME_DATA_NEGATIVE)
        self.client.post(
            '/meme',
            json=data,
            headers=self.headers
        )

    @task(3)
    def change_meme(self):
        if self.meme_id:
            data = random.choice(MEME_DATA_POSITIVE)
            meme_id = random.choice(self.meme_id)
            self.client.put(
                f'/meme/{meme_id}',
                json=data,
                headers=self.headers
            )

    @task(1)
    def change_meme_with_negative_data(self):
        if self.meme_id:
            data = random.choice(MEME_DATA_NEGATIVE)
            meme_id = self.meme_id[0]
            self.client.put(
                f'/meme/{meme_id}',
                json=data,
                headers=self.headers
            )

    @task(1)
    def delete_meme(self):
        if self.meme_id:
            meme_id = random.choice(self.meme_id)
            response = self.client.delete(
                f'/meme/{meme_id}',
                headers=self.headers
            )
            if response.status_code == 204:
                self.meme_id.remove(meme_id)

    @task(1)
    def delete_non_existent_meme(self):
        fake_id = 999999
        self.client.delete(
            f'/meme/{fake_id}',
            headers=self.headers
        )

    def on_stop(self):
        for meme_id in self.meme_id:
            self.client.delete(f'/meme/{meme_id}', headers=self.headers)
        self.meme_id.clear()
