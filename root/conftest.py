import pytest
import requests
from root.endpoints.authorize_user import AuthorizeUser
from root.endpoints.check_token import CheckExistingToken
from root.endpoints.create_meme import CreateMeme
from root.endpoints.delete_meme import DeleteMeme
from root.endpoints.change_meme import FullChangeMeme
from root.endpoints.get_all_memes import GetAllMemes
from root.endpoints.get_one_meme import GetOneMeme
from root.data.test_parameters import CREDENTIALS_FILE, USERNAME


@pytest.fixture()
def set_token(authorize_endpoint):
    def _set_token(endpoint):
        endpoint.token = authorize_endpoint.token
        return endpoint
    return _set_token


@pytest.fixture(scope="session")
def authorize_endpoint(get_token_endpoint):
    authorized_user = AuthorizeUser(CREDENTIALS_FILE, USERNAME)
    authorized_user.get_token()
    if not get_token_endpoint.is_token_alive():
        authorized_user.get_new_token()
    return authorized_user


@pytest.fixture(scope="session")
def get_token_endpoint():
    return CheckExistingToken()


@pytest.fixture()
def get_memes_endpoint(set_token):
    return set_token(GetAllMemes())


@pytest.fixture()
def get_meme_by_id_endpoint(set_token):
    return set_token(GetOneMeme())


@pytest.fixture()
def create_meme_endpoint(set_token):
    created_meme = set_token(CreateMeme())
    yield created_meme
    requests.delete(
        f"{created_meme.url}meme/{created_meme.meme_id}",
        headers={"Authorization": created_meme.token}
    )
    if created_meme.duplicate_id is not None:
        requests.delete(
            f"{created_meme.url}meme/{created_meme.duplicate_id}",
            headers={"Authorization": created_meme.token}
        )


@pytest.fixture()
def change_meme_endpoint(set_token):
    changing_meme = set_token(FullChangeMeme(USERNAME))
    return changing_meme


@pytest.fixture()
def delete_meme_endpoint(set_token):
    deleting_meme = set_token(DeleteMeme())
    return deleting_meme
