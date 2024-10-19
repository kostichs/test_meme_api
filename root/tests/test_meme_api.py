import pytest
import requests
import json
import os


def load_meme_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

MEME_DATA = load_meme_data(os.path.join(os.path.dirname(__file__), '../data/create_meme_data.json'))


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()


@pytest.mark.parametrize('meme_id', [1, 2, 3, 4, 5])
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_create_meme(create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(meme)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_completely_change_meme(fully_change_meme, create_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    fully_change_meme.change_meme(data=meme, meme_id=create_meme_endpoint.response.json()['id'])

@pytest.mark.parametrize("meme", MEME_DATA)
def test_delete_meme(create_meme_endpoint, delete_meme_endpoint, meme):
    create_meme_endpoint.create_a_meme(data=meme)
    delete_meme_endpoint.delete_meme(create_meme_endpoint.response.json()['id'])
