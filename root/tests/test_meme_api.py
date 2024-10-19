import pytest
import requests
import json
import os


def load_meme_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

MEME_DATA = load_meme_data(os.path.join(os.path.dirname(__file__), '../data/meme_structure.json'))


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()


@pytest.mark.parametrize('meme_id', [1, 2, 3, 4, 5])
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)


@pytest.mark.parametrize("meme", MEME_DATA)
def test_create_meme(create_meme_endpoint, meme):
    data = {
        "url": meme["url"],
        "text": meme["text"],
        "tags": meme["tags"],
        "info": meme["info"]
    }
    create_meme_endpoint.create_a_meme(data)

    response = requests.delete(
        f"{create_meme_endpoint.url}meme/{create_meme_endpoint.response.json()['id']}",
        headers={"Authorization": create_meme_endpoint.token}
    )
    assert response.status_code == 200
