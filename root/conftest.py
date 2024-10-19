import pytest
from root.endpoints.authorize_user import AuthorizeUser
from root.endpoints.check_token import CheckExistingToken


@pytest.fixture(scope="session")
def authorize_user_endpoint(get_existing_token_endpoint):
    authorized_user = AuthorizeUser()
    token = authorized_user.get_token()
    print(token)
    if not get_existing_token_endpoint.is_token_alive(token):
        authorized_user.get_new_token()
    print("Token:", authorized_user.token)
    return authorized_user


@pytest.fixture(scope="session")
def get_existing_token_endpoint():
    return CheckExistingToken()
