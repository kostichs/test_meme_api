import pytest


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()

@pytest.mark.parametrize('meme_id', [1, 2, 3, 4, 5])
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)
