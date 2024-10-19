import pytest
from root.endpoints.authorize_user import AuthorizeUser


@pytest.fixture(scope="session")
def authorize_user_endpoint():
    authorized_user = AuthorizeUser()
    return authorized_user
