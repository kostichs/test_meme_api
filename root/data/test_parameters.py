import os
import json
import random


def load_meme_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


MEME_DATA_POSITIVE = load_meme_data(os.path.join(os.path.dirname(__file__), 'positive_meme_data.json'))
MEME_DATA_NEGATIVE = load_meme_data(os.path.join(os.path.dirname(__file__), 'negative_meme_data.json'))
MEME_CHANGE_DATA = load_meme_data(os.path.join(os.path.dirname(__file__), 'changing_meme_data.json'))
MEME_RANDOM = random.choice(MEME_DATA_POSITIVE)
MEME_KEYS = ['id', 'url', 'text', 'tags', 'info']
MEME_IDS = [1, 2, 3, 4, 5]
CREDENTIALS_FILE = 'credentials.json'
USERNAME = 'sergey'
MAX_TIME = 2