import pytest
import allure

from root.data.htttp_enum import HTTPStatus
from root.data.test_parameters import (MEME_DATA_POSITIVE, MEME_DATA_NEGATIVE, MEME_CHANGE_DATA,
                                       MAX_TIME, MEME_KEYS, MEME_IDS)


@pytest.mark.skip('Reason: to avoid overloading of new tokens on server. Use only if necessary')
@allure.feature('Authorization')
@allure.story('User authorization')
@allure.title('Test user authorization flow')
def test_authorize_user(authorize_endpoint):
    authorize_endpoint.get_new_token()
    authorize_endpoint.check_response(HTTPStatus.OK)
    authorize_endpoint.get_token()

    authorize_endpoint.check_token()
    authorize_endpoint.check_username()
    authorize_endpoint.check_response_time(MAX_TIME)


@allure.feature('Memes')
@allure.story('Get all memes')
@allure.title('Test get all memes')
def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_response(HTTPStatus.OK)
    get_memes_endpoint.check_response_not_empty()
    get_memes_endpoint.check_response_structure(MEME_KEYS)
    get_memes_endpoint.check_response_time(MAX_TIME)


@allure.feature('Memes')
@allure.story('Negative cases for get memes')
@allure.title('Test get all memes with negative cases')
def test_get_all_memes_unauthorized(get_memes_endpoint):
    get_memes_endpoint.get_all_memes(authorized=False)
    get_memes_endpoint.check_response(HTTPStatus.UNAUTHORIZED)


@allure.feature('Memes')
@allure.story('Get a meme by ID')
@allure.title('Test get one meme by ID')
def test_get_meme_by_id(create_default_meme, get_meme_by_id_endpoint, ):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id=create_default_meme.meme_id)
    get_meme_by_id_endpoint.check_response(HTTPStatus.OK)
    get_meme_by_id_endpoint.check_id(meme_id=create_default_meme.meme_id)
    get_meme_by_id_endpoint.check_response_not_empty()
    get_meme_by_id_endpoint.check_response_structure(MEME_KEYS)
    get_meme_by_id_endpoint.check_response_time(MAX_TIME)


@pytest.mark.parametrize('invalid_id', [999999, "invalid_id", -1, 0, None])
@allure.feature('Memes')
@allure.story('Negative cases for get meme by ID')
@allure.title('Test get one meme with invalid IDs')
def test_get_one_meme_with_negative_id(get_meme_by_id_endpoint, invalid_id):
    get_meme_by_id_endpoint.get_meme_by_id(invalid_id)
    get_meme_by_id_endpoint.check_response(HTTPStatus.NOT_FOUND)


@pytest.mark.parametrize('meme_id', MEME_IDS)
@allure.feature('Memes')
@allure.story('Unauthorized access for get meme')
@allure.title('Test get meme unauthorized')
def test_get_meme_unauthorized(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id=meme_id, authorized=False)
    get_meme_by_id_endpoint.check_response(HTTPStatus.UNAUTHORIZED)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Create meme')
@allure.title('Test create meme')
def test_create_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_response(HTTPStatus.OK)
    create_meme_endpoint.check_response_time(MAX_TIME)
    create_meme_endpoint.check_response_values(meme)
    create_meme_endpoint.check_response_structure(MEME_KEYS)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Create a duplicate')
@allure.title('Test create meme')
def test_create_duplicated_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_response(HTTPStatus.OK)


@pytest.mark.parametrize("meme", MEME_DATA_NEGATIVE)
@allure.feature('Memes')
@allure.story('Create meme with invalid data')
@allure.title('Test create meme with invalid data')
def test_create_meme_with_invalid_data(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)
    create_meme_endpoint.check_response(HTTPStatus.BAD_REQUEST)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Unauthorized access for create meme')
@allure.title('Test create meme unauthorized')
def test_create_meme_unauthorized(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme, authorized=False)
    create_meme_endpoint.check_response(HTTPStatus.UNAUTHORIZED)


@pytest.mark.smoke
@pytest.mark.parametrize("meme", MEME_CHANGE_DATA)
@allure.feature('Memes')
@allure.story('Change meme')
@allure.title('Test change meme')
def test_change_meme(change_meme_endpoint, create_default_meme, meme):
    change_meme_endpoint.change_meme(data=meme, meme_id=create_default_meme.meme_id)
    change_meme_endpoint.check_response(HTTPStatus.OK)
    change_meme_endpoint.check_changer_name()
    change_meme_endpoint.check_response_values(data=meme)
    change_meme_endpoint.check_response_structure(meme.keys())
    change_meme_endpoint.check_response_time(MAX_TIME)


@pytest.mark.parametrize("meme", MEME_DATA_POSITIVE)
@allure.feature('Memes')
@allure.story('Unauthorized access for change meme')
@allure.title('Test change meme unauthorized')
def test_change_meme_unauthorized(change_meme_endpoint, create_default_meme, meme):
    change_meme_endpoint.change_meme(data=meme, meme_id=create_default_meme.meme_id, authorized=False)
    change_meme_endpoint.check_response(HTTPStatus.UNAUTHORIZED)
    # TODO: добавить изменение существующего мема, но не являющегося твоим


@pytest.mark.parametrize("valid_meme, invalid_meme", zip(MEME_DATA_POSITIVE, MEME_DATA_NEGATIVE))
@allure.feature('Memes')
@allure.story('Change meme with invalid data')
@allure.title('Test change meme with invalid data')
def test_change_meme_with_invalid_data(change_meme_endpoint, create_default_meme, valid_meme, invalid_meme):
    change_meme_endpoint.change_meme(data=invalid_meme, meme_id=create_default_meme.meme_id)
    change_meme_endpoint.check_response(HTTPStatus.BAD_REQUEST)


@allure.feature('Memes')
@allure.story('Delete meme')
@allure.title('Test delete meme')
def test_delete_meme(create_default_meme, delete_meme_endpoint, get_meme_by_id_endpoint):
    delete_meme_endpoint.delete_meme(meme_id=create_default_meme.meme_id)
    delete_meme_endpoint.check_response(HTTPStatus.OK)
    delete_meme_endpoint.check_response_time(MAX_TIME)
    get_meme_by_id_endpoint.get_meme_by_id(meme_id=create_default_meme.meme_id)
    get_meme_by_id_endpoint.check_response(HTTPStatus.NOT_FOUND)


@allure.feature('Memes')
@allure.story('Negative cases for delete meme unauthorized and with re-deletion')
@allure.title('Test delete meme with negative case')
def test_delete_meme_unauthorized(create_default_meme, delete_meme_endpoint):
    delete_meme_endpoint.delete_meme(meme_id=create_default_meme.meme_id, authorized=False)
    delete_meme_endpoint.check_response(HTTPStatus.UNAUTHORIZED)


@pytest.mark.parametrize('fake_id', [999999, "invalid_id", -1, None])
@allure.feature('Memes')
@allure.story('Delete meme with invalid IDs')
@allure.title('Test delete meme with fake IDs')
def test_delete_meme_with_fake_id(delete_meme_endpoint, fake_id):
    delete_meme_endpoint.delete_meme(meme_id=fake_id)
    delete_meme_endpoint.check_response(HTTPStatus.NOT_FOUND)
