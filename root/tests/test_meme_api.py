import pytest
import requests


def test_get_all_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()


@pytest.mark.parametrize('meme_id', [1, 2, 3, 4, 5])
def test_get_one_meme(get_meme_by_id_endpoint, meme_id):
    get_meme_by_id_endpoint.get_one_meme(meme_id=meme_id)


def test_create_meme(create_meme_endpoint):
    info = {
        "colors": [
            "green",
            "black",
            "white"
        ],
        "objects": [
            "picture",
            "text"
        ]
    }
    tags = [
        "fun",
        "yoda"
    ]
    url = 'https://i.pinimg.com/originals/a6/56/23/a65623b21bd407284697726d01f39c7e.jpg'
    text = "Sample text"
    data = {"url": url, "text": text, "tags": tags, "info": info}
    create_meme_endpoint.create_a_meme(data)
    response = requests.delete(f"{create_meme_endpoint.url}meme/{create_meme_endpoint.response.json()['id']}", headers={"Authorization": create_meme_endpoint.token})
