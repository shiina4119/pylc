import requests
from . import generate_headers, GRAPHQL_URL


def fetch_daily() -> int:
    headers = generate_headers()
    query = """
    query {
      activeDailyCodingChallengeQuestion {
        question {
          questionFrontendId
        }
      }
    }
    """

    response = requests.post(url=GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    return int(
        json["data"]["activeDailyCodingChallengeQuestion"]["question"][
            "questionFrontendId"
        ]
    )


def fetch_problem_content(title_slug: str) -> str:
    headers = generate_headers()
    query = """
    query ($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
      }
    }
    """
    variables = {"titleSlug": title_slug}
    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    return json["data"]["question"]["content"]


def fetch_problem_snippets(title_slug: str) -> dict:
    headers = generate_headers()
    query = """
    query ($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        codeSnippets {
          langSlug
          code
        }
      }
    }       
    """
    variables = {"titleSlug": title_slug}
    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()

    snippets = {
        snippet_map["langSlug"]: snippet_map["code"]
        for snippet_map in json["data"]["question"]["codeSnippets"]
    }

    return snippets


def fetch_problem_testcases(title_slug: str) -> str:
    headers = generate_headers()
    query = """
    query ($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        exampleTestcaseList
      }
    }
    """
    variables = {"titleSlug": title_slug}

    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    return json["data"]["question"]["exampleTestcaseList"]
