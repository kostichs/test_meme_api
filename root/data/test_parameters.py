import os
import json


def load_meme_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


MEME_DATA = load_meme_data(os.path.join(os.path.dirname(__file__), 'create_meme_data.json'))
MEME_KEYS = ['id', 'url', 'text', 'tags', 'info']
MEME_IDS = [1, 2, 3, 4, 5]
