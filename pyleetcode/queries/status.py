import requests
from time import sleep
from . import generate_headers, BASE_URL


def get_status(title_slug: str, id: str, test: bool = True) -> dict:
    url = f"{BASE_URL}/submissions/detail/{id}/check/"

    headers = generate_headers()
    headers["Referer"] = f"{BASE_URL}/problems/{title_slug}"
    if test:
        headers["Referer"] += "/submissions"

    while True:
        response = requests.post(url=url, headers=headers)
        sleep(1)
        json = response.json()
        if json["state"] == "SUCCESS":
            break

    return json
