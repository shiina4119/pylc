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


def fetch_problem(title_slug: str) -> dict:
    headers = generate_headers()
    query = """
    query ($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        difficulty
        content
        mysqlSchemas
        exampleTestcaseList
        topicTags {
          name
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
    return json["data"]["question"]
