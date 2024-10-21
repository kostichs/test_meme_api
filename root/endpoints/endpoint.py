import allure


class Endpoint:
    CREDENTIALS_FILE = 'credentials.json'
    USERNAME = 'sergey'
    url = 'http://167.172.172.115:52355/'
    max_time = 2
    response = None

    @property
    def token(self):
        return Endpoint.token

    @token.setter
    def token(self, value):
        Endpoint.token = value

    @allure.step('Check 200 status code')
    def check_response_200(self):
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check 400 status code')
    def check_response_400(self):
        assert self.response.status_code == 400, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check 401 status code')
    def check_response_401(self):
        assert self.response.status_code == 401, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check 404 status code')
    def check_response_404(self):
        assert self.response.status_code == 404, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check response time')
    def check_response_time(self):
        assert self.response.elapsed.total_seconds() < self.max_time, \
            f"Response took too long: {self.response.elapsed.total_seconds()} seconds"
