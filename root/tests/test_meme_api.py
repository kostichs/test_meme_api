import requests

from root.conftest import authorize_endpoint


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()


def test_get_one_meme(authorize_endpoint):
    ...