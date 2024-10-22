import pytest
from root.endpoints.authorize_user import AuthorizeUser
from root.endpoints.check_token import CheckExistingToken
from root.endpoints.create_meme import CreateMeme
from root.endpoints.delete_meme import DeleteMeme
from root.endpoints.change_meme import FullChangeMeme
from root.endpoints.get_all_memes import GetAllMemes
from root.endpoints.get_one_meme import GetOneMeme
from root.data.test_parameters import CREDENTIALS_FILE, USERNAME, MEME_DATA_POSITIVE


@pytest.fixture()
def token(authorize_endpoint):
    token = authorize_endpoint.token
    return token


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
def get_memes_endpoint(token):
    return GetAllMemes(token)


@pytest.fixture()
def get_meme_by_id_endpoint(token):
    return GetOneMeme(token)


@pytest.fixture()
def create_meme_endpoint(token, delete_meme_endpoint):
    created_meme = CreateMeme(token)
    yield created_meme
    if created_meme.meme_id:
        delete_meme_endpoint.delete_meme(created_meme.meme_id)

@pytest.fixture()
def change_meme_endpoint(token):
    changing_meme = FullChangeMeme(USERNAME, token)
    return changing_meme


@pytest.fixture()
def delete_meme_endpoint(token):
    deleting_meme = DeleteMeme(token)
    return deleting_meme


@pytest.fixture()
def create_default_meme(token):
    default_meme = CreateMeme(token)
    default_meme.create_a_meme(MEME_DATA_POSITIVE[0])
    return default_meme
