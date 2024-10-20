import pytest
from root.data.test_parameters import MEME_DATA, MEME_KEYS, MEME_IDS


@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
def test_authorize_user(authorize_endpoint):
    authorize_endpoint.get_new_token()
    authorize_endpoint.get_old_token()
    authorize_endpoint.check_response_200()
    authorize_endpoint.check_token()
    authorize_endpoint.check_username()
    authorize_endpoint.check_response_time()


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_response_200()
    get_memes_endpoint.check_response_not_empty()
    get_memes_endpoint.check_response_structure(MEME_KEYS)
    get_memes_endpoint.check_response_time()


@pytest.mark.parametrize('data', ["invalid_url", "meme01", None])
def test_get_all_memes_with_negative_cases(get_memes_endpoint, data):
    get_memes_endpoint.check_unauthorized_access()
    get_memes_endpoint.check_invalid_url(data)


@pytest.mark.parametrize('meme_id', MEME_IDS)
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)
    get_meme_by_id_endpoint.check_response_200()
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
    create_meme_endpoint.check_response_200()
    create_meme_endpoint.check_response_time()
    create_meme_endpoint.check_response_values(meme)
    create_meme_endpoint.check_response_structure(MEME_KEYS)
    create_meme_endpoint.check_duplicate_creation(meme)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_create_meme_unauthorized(create_meme_endpoint, meme):
    create_meme_endpoint.create_meme_unauthorized(meme)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_completely_change_meme(fully_change_meme, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    fully_change_meme.change_meme(data=meme, meme_id=create_meme_endpoint.get_meme_id)
    fully_change_meme.check_response_200()
    fully_change_meme.check_response_values(meme)
    fully_change_meme.check_response_structure(meme.keys())
    fully_change_meme.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA)
def test_delete_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_response_200()
    delete_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA)
def test_delete_meme_with_negative_case(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme_unauthorized(meme_id)
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_negative_deletion(meme_id)


@pytest.mark.parametrize('fake_id', [999999, "invalid_id", -1])
def test_delete_meme_with_fake_id(delete_meme_endpoint, fake_id):
    delete_meme_endpoint.check_negative_deletion(fake_id)
