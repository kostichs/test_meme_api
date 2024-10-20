import pytest
import requests
from root.endpoints.authorize_user import AuthorizeUser
from root.endpoints.check_token import CheckExistingToken
from root.endpoints.create_meme import CreateMeme
from root.endpoints.delete_meme import DeleteMeme
from root.endpoints.change_meme import FullChangeMeme
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
    yield created_meme
    if created_meme.meme_id is not None:
        for _id in created_meme.meme_id:
            requests.delete(
                f"{created_meme.url}meme/{_id}",
                headers={"Authorization": created_meme.token}
            )


@pytest.fixture()
def change_meme_endpoint(authorize_endpoint):
    changing_meme = FullChangeMeme()
    changing_meme.token = authorize_endpoint.token
    return changing_meme


@pytest.fixture()
def delete_meme_endpoint(authorize_endpoint):
    deleting_meme = DeleteMeme()
    deleting_meme.token = authorize_endpoint.token
    return deleting_meme
