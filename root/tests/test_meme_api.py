import pytest
from root.data.test_parameters import MEME_DATA_POSITIVE, MEME_KEYS, MEME_IDS, MEME_DATA_NEGATIVE


@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
def test_authorize_user(authorize_endpoint):
    authorize_endpoint.get_new_token()
    authorize_endpoint.get_old_token()
    authorize_endpoint.check_token()
    authorize_endpoint.check_username()
    authorize_endpoint.check_response_time()


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
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
    get_meme_by_id_endpoint.check_response_not_empty()
    get_meme_by_id_endpoint.check_response_structure(MEME_KEYS)
    get_meme_by_id_endpoint.check_response_time()


@pytest.mark.parametrize('invalid_id', [999999, "invalid_id", None])
def test_get_one_meme_with_negative_data(get_meme_by_id_endpoint, invalid_id):
    get_meme_by_id_endpoint.check_meme_not_found(invalid_id)


@pytest.mark.parametrize('meme_id', MEME_IDS)
def test_get_meme_unauthorized(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.check_unauthorized_access(meme_id=meme_id)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_create_meme(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_response_time()
    create_meme_endpoint.check_response_values(meme)
    create_meme_endpoint.check_response_structure(MEME_KEYS)
    create_meme_endpoint.check_duplicate_creation(meme)


@pytest.mark.parametrize("meme", MEME_DATA_NEGATIVE)
def test_create_meme_with_invalid_data(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme_with_invalid_data(meme)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_create_meme_unauthorized(create_meme_endpoint, meme):
    create_meme_endpoint.create_meme_unauthorized(meme)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_change_meme(change_meme_endpoint, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    change_meme_endpoint.change_meme(data=meme, meme_id=create_meme_endpoint.get_meme_id)
    change_meme_endpoint.check_changer_name()
    change_meme_endpoint.check_response_values(meme)
    change_meme_endpoint.check_response_structure(meme.keys())
    change_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_change_meme_unauthorized(change_meme_endpoint, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    change_meme_endpoint.change_meme_unauthorized(data=meme, meme_id=create_meme_endpoint.get_meme_id)


@pytest.mark.parametrize("valid_meme, invalid_meme",
                         [(positive, negative) for positive, negative in zip(MEME_DATA_POSITIVE, MEME_DATA_NEGATIVE)])
def test_change_meme_with_invalid_datas(change_meme_endpoint, create_meme_endpoint, valid_meme, invalid_meme):
    create_meme_endpoint.create_a_meme(valid_meme)
    change_meme_endpoint.check_invalid_data(data=invalid_meme, meme_id=create_meme_endpoint.get_meme_id)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_delete_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
def test_delete_meme_with_negative_case(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme_unauthorized(meme_id)
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_negative_deletion(meme_id)


@pytest.mark.parametrize('fake_id', [999999, "invalid_id", -1])
def test_delete_meme_with_fake_id(delete_meme_endpoint, fake_id):
    delete_meme_endpoint.check_negative_deletion(fake_id)
