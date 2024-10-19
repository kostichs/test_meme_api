import pytest
from root.endpoints.authorize_user import AuthorizeUser
from root.endpoints.check_token import CheckExistingToken
from root.endpoints.create_meme import CreateMeme
from root.endpoints.get_all_memes import GetAllMemes
from root.endpoints.get_one_meme import GetOneMeme


@pytest.fixture(scope="session")
def authorize_endpoint(get_token_endpoint):
    authorized_user = AuthorizeUser()
    token = authorized_user.get_old_token()
    if not get_token_endpoint.is_token_alive(token):
        authorized_user.get_new_token()
    return authorized_user


@pytest.fixture(scope="session")
def get_token_endpoint():
    return CheckExistingToken()


@pytest.fixture()
def get_memes_endpoint(authorize_endpoint):
    all_memes = GetAllMemes()
    all_memes.token = authorize_endpoint.token
    return all_memes


@pytest.fixture()
def get_meme_by_id_endpoint(authorize_endpoint):
    meme = GetOneMeme()
    meme.token = authorize_endpoint.token
    return meme

@pytest.fixture()
def create_meme_endpoint(authorize_endpoint):
    created_meme = CreateMeme()
    created_meme.token = authorize_endpoint.token
    return created_meme
