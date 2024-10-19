import requests


def test_get_all_memes(authorize_user_endpoint):
    response = requests.get(
        "http://167.172.172.115:52355/meme",
        headers={"Authorization":authorize_user_endpoint.token})
    print(response)
