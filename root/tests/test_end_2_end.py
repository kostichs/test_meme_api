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
    meme_id = create_meme_endpoint.meme_id
    get_meme_by_id_endpoint.get_one_meme(meme_id)
    change_meme_endpoint.change_meme(data=meme, meme_id=meme_id)
    delete_meme_endpoint.delete_meme(meme_id=meme_id)