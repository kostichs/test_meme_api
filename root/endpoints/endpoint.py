import allure


class Endpoint:
    url = 'http://167.172.172.115:52355/'
    response = None
    response_json = None
    token = None
    headers = None
    default_data = None
    max_time = 2

    @allure.step('Check if authorization was successful')
    def check_success(self):
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"

    @allure.step('Check response time')
    def check_response_time(self):
        assert self.response.elapsed.total_seconds() < self.max_time, \
            f"Response took too long: {self.response.elapsed.total_seconds()} seconds"
