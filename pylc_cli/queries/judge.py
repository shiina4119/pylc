import requests
import json
from . import generate_headers, BASE_URL
from .fetch_problem import fetch_problem_testcases


def send_judge(title_slug: str, id: int, lang: str, typed_code: str, test: bool):
    url = f"{BASE_URL}/problems/{title_slug}"
    if test:
        url += "/interpret_solution/"
    else:
        url += "/submit/"

    headers = generate_headers()
    headers["Referer"] = f"{BASE_URL}/problems/{title_slug}"

    test_cases = fetch_problem_testcases(title_slug=title_slug)

    payload = {
        "lang": lang,
        "question_id": id,
        "typed_code": typed_code,
    }

    if test:
        input_str = ""
        for i in test_cases:
            input_str += i + "\n"

        payload["data_input"] = input_str

    response = requests.post(url=url, headers=headers, data=json.dumps(payload))

    _json = response.json()
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    if test:
        return _json["interpret_id"]
    else:
        return _json["submission_id"]
