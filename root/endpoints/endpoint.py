import allure
from enum import Enum


class Endpoint:
    url = 'http://167.172.172.115:52355/'
    response = None

    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token

    def check_response(self, status: Enum):
        with allure.step(f"Check {status.name} status code"):
            assert self.response.status_code == status.value, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check response time')
    def check_response_time(self, max_time):
        assert self.response.elapsed.total_seconds() < max_time, \
            f"Response took too long: {self.response.elapsed.total_seconds()} seconds"
