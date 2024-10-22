import allure

from root.data.htttp_enum import HTTPStatus
from enum import Enum


class Endpoint:
    url = 'http://167.172.172.115:52355/'
    max_time = 2
    response = None

    def __init__(self, username=None):
        self.username = username

    @property
    def token(self):
        return Endpoint.token

    @token.setter
    def token(self, value):
        Endpoint.token = value

    def check_response(self, status: Enum):
        with allure.step(f"Check {status.name} status code"):
            assert self.response.status_code == status.value, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check response time')
    def check_response_time(self):
        assert self.response.elapsed.total_seconds() < self.max_time, \
            f"Response took too long: {self.response.elapsed.total_seconds()} seconds"
