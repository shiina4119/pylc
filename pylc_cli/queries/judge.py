import requests
import json
from . import generate_headers, BASE_URL
from .fetch_question import fetch_question


def send_judge(title_slug: str, lang: str, typed_code: str, test: bool):
    url = f"{BASE_URL}/problems/{title_slug}"
    if test:
        url += "/interpret_solution/"
    else:
        url += "/submit/"

    headers = generate_headers()
    headers["Referer"] = f"{BASE_URL}/problems/{title_slug}"

    question = fetch_question(title_slug=title_slug)
    questionId = question["questionId"]

    payload = {
        "lang": lang,
        "question_id": questionId,
        "typed_code": typed_code,
    }

    if test:
        input_str = ""
        for i in question["exampleTestcaseList"]:
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
