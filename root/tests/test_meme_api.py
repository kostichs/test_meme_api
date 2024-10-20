import pytest
from root.data.test_parameters import MEME_DATA, MEME_KEYS, MEME_IDS


@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
def test_authorize_user(authorize_endpoint):
    authorize_endpoint.get_new_token()
    authorize_endpoint.get_old_token()
    authorize_endpoint.check_success()
    authorize_endpoint.check_token()
    authorize_endpoint.check_username()
    authorize_endpoint.check_response_time()


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_success()
    get_memes_endpoint.check_response_not_empty()
    get_memes_endpoint.check_response_structure(MEME_KEYS)
    get_memes_endpoint.check_response_time()


def test_get_all_memes_with_negative_cases(get_memes_endpoint):
    get_memes_endpoint.check_unauthorized_access()
    get_memes_endpoint.check_invalid_url()


@pytest.mark.parametrize('meme_id', MEME_IDS)
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)
    get_meme_by_id_endpoint.check_success()
    get_meme_by_id_endpoint.check_response_not_empty()
    get_meme_by_id_endpoint.check_response_structure(MEME_KEYS)
    get_meme_by_id_endpoint.check_response_time()


@pytest.mark.parametrize('invalid_id', [999999, "invalid_id", None])
def test_get_one_meme_with_negative_data(get_meme_by_id_endpoint, invalid_id):
    get_meme_by_id_endpoint.check_meme_not_found(invalid_id)


@pytest.mark.parametrize('meme_id', MEME_IDS)
def test_get_meme_unauthorized(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.check_unauthorized_access(meme_id=meme_id)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_create_meme(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_success()
    create_meme_endpoint.check_response_values(meme)
    create_meme_endpoint.check_response_structure(MEME_KEYS)
    create_meme_endpoint.check_duplicate_creation(meme)
    create_meme_endpoint.create_meme_with_unauthorized_user(meme)
    create_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA)
def test_completely_change_meme(fully_change_meme, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    fully_change_meme.change_meme(data=meme, meme_id=create_meme_endpoint.meme_id)
    fully_change_meme.check_success()
    fully_change_meme.check_response_values(meme)
    fully_change_meme.check_response_structure(meme.keys())
    fully_change_meme.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA)
def test_delete_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.meme_id
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_success()
    delete_meme_endpoint.check_response_time()

    delete_meme_endpoint.check_meme_deleted(meme_id)
    delete_meme_endpoint.delete_non_existing_meme(meme_id)
    delete_meme_endpoint.delete_meme_with_invalid_id("invalid_id")
    delete_meme_endpoint.delete_meme_without_auth(meme_id)

