import pytest
import allure
import random
from root.data.test_parameters import MEME_DATA_POSITIVE, MEME_KEYS, MEME_IDS, MEME_DATA_NEGATIVE


@pytest.mark.smoke
@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
@allure.feature('End-to-End Flow')
@allure.story('Complete meme lifecycle')
@allure.title('Test end-to-end meme lifecycle')
@pytest.mark.parametrize("meme", [random.choice(MEME_DATA_POSITIVE)])
def test_end_to_end(authorize_endpoint, create_meme_endpoint, get_memes_endpoint,
                    change_meme_endpoint, get_meme_by_id_endpoint, delete_meme_endpoint, meme):
    authorize_endpoint.get_new_token()
    get_memes_endpoint.get_all_memes()
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    get_meme_by_id_endpoint.get_one_meme(meme_id)
    change_meme_endpoint.change_meme(data=meme, meme_id=meme_id)
    delete_meme_endpoint.delete_meme(meme_id=meme_id)


@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
@allure.feature('Authorization')
@allure.story('User authorization')
@allure.title('Test user authorization flow')
def test_authorize_user(authorize_endpoint):
    authorize_endpoint.get_new_token()
    authorize_endpoint.get_old_token()
    authorize_endpoint.check_token()
    authorize_endpoint.check_username()
    authorize_endpoint.check_response_time()


@allure.feature('Memes')
@allure.story('Get all memes')
@allure.title('Test get all memes')
def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_response_not_empty()
    get_memes_endpoint.check_response_structure(MEME_KEYS)
    get_memes_endpoint.check_response_time()


@pytest.mark.parametrize('data', ["invalid_url", "meme01", None])
@allure.feature('Memes')
@allure.story('Negative cases for get memes')
@allure.title('Test get all memes with negative cases')
def test_get_all_memes_with_negative_cases(get_memes_endpoint, data):
    get_memes_endpoint.check_unauthorized_access()
    get_memes_endpoint.check_invalid_url(data)


@pytest.mark.parametrize('meme_id', MEME_IDS)
@allure.feature('Memes')
@allure.story('Get a meme by ID')
@allure.title('Test get one meme by ID')
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)
    get_meme_by_id_endpoint.check_response_not_empty()
    get_meme_by_id_endpoint.check_response_structure(MEME_KEYS)
    get_meme_by_id_endpoint.check_response_time()


@pytest.mark.parametrize('invalid_id', [999999, "invalid_id", -1, 0, None])
@allure.feature('Memes')
@allure.story('Negative cases for get meme by ID')
@allure.title('Test get one meme with invalid IDs')
def test_get_one_meme_with_negative_data(get_meme_by_id_endpoint, invalid_id):
    get_meme_by_id_endpoint.check_meme_not_found(invalid_id)


@pytest.mark.parametrize('meme_id', MEME_IDS)
@allure.feature('Memes')
@allure.story('Unauthorized access for get meme')
@allure.title('Test get meme unauthorized')
def test_get_meme_unauthorized(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.check_unauthorized_access(meme_id=meme_id)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Create meme')
@allure.title('Test create meme')
def test_create_meme(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_response_time()
    create_meme_endpoint.check_response_values(meme)
    create_meme_endpoint.check_response_structure(MEME_KEYS)
    create_meme_endpoint.check_duplicate_creation(meme)


@pytest.mark.parametrize("meme", MEME_DATA_NEGATIVE)
@allure.feature('Memes')
@allure.story('Create meme with invalid data')
@allure.title('Test create meme with invalid data')
def test_create_meme_with_invalid_data(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme_with_invalid_data(meme)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Unauthorized access for create meme')
@allure.title('Test create meme unauthorized')
def test_create_meme_unauthorized(create_meme_endpoint, meme):
    create_meme_endpoint.create_meme_unauthorized(meme)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Change meme')
@allure.title('Test change meme')
def test_change_meme(change_meme_endpoint, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    change_meme_endpoint.change_meme(data=meme, meme_id=create_meme_endpoint.get_meme_id)
    change_meme_endpoint.check_changer_name()
    change_meme_endpoint.check_response_values(meme)
    change_meme_endpoint.check_response_structure(meme.keys())
    change_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Unauthorized access for change meme')
@allure.title('Test change meme unauthorized')
def test_change_meme_unauthorized(change_meme_endpoint, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    change_meme_endpoint.change_meme_unauthorized(data=meme, meme_id=create_meme_endpoint.get_meme_id)


@pytest.mark.parametrize("valid_meme, invalid_meme",
                         [(positive, negative) for positive, negative in zip(MEME_DATA_POSITIVE, MEME_DATA_NEGATIVE)])
@allure.feature('Memes')
@allure.story('Change meme with invalid data')
@allure.title('Test change meme with invalid data')
def test_change_meme_with_invalid_datas(change_meme_endpoint, create_meme_endpoint, valid_meme, invalid_meme):
    create_meme_endpoint.create_a_meme(valid_meme)
    change_meme_endpoint.check_invalid_data(data=invalid_meme, meme_id=create_meme_endpoint.get_meme_id)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Delete meme')
@allure.title('Test delete meme')
def test_delete_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_response_time()


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Negative cases for delete meme')
@allure.title('Test delete meme with negative case')
def test_delete_meme_with_negative_case(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    meme_id = create_meme_endpoint.get_meme_id
    delete_meme_endpoint.delete_meme_unauthorized(meme_id)
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_negative_deletion(meme_id)


@pytest.mark.parametrize('fake_id', [999999, "invalid_id", -1, None])
@allure.feature('Memes')
@allure.story('Delete meme with invalid IDs')
@allure.title('Test delete meme with fake IDs')
def test_delete_meme_with_fake_id(delete_meme_endpoint, fake_id):
    delete_meme_endpoint.check_negative_deletion(fake_id)
