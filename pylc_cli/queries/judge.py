import json

import aiohttp

from . import BASE_URL, headers
from .graphql import fetch_problem_testcases


async def send_judge(
    title_slug: str, id: int, lang: str, typed_code: str, test: bool
) -> str:
    url = f"{BASE_URL}/problems/{title_slug}"
    if test:
        url += "/interpret_solution/"
    else:
        url += "/submit/"

    headers["Referer"] = f"{BASE_URL}/problems/{title_slug}"

    test_cases = await fetch_problem_testcases(title_slug=title_slug)

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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url, data=json.dumps(payload), headers=headers
        ) as response:
            if response.status != 200:
                # TODO: handle 403 errors nicely
                raise ConnectionError

            _json = await response.json()
            if test:
                return _json["interpret_id"]
            else:
                return _json["submission_id"]
