import requests
from . import GRAPHQL_URL, generate_headers


def fetch_all_problems_count() -> int:
    headers = generate_headers()
    query = """
    query {
      allQuestionsCount {
        count
      }
    }
    """
    response = requests.post(url=GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    count = json["data"]["allQuestionsCount"][0]["count"]
    return count


def fetch_all_problems_metadata(count: int) -> dict:
    headers = generate_headers()
    query = """
    query ($categorySlug: String
    $limit: Int
    $skip: Int
    $filters: QuestionListFilterInput) {
      questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        totalNum
        data {
          questionFrontendId,
          questionId,
          title,
          titleSlug,
          difficulty,
          isPaidOnly,
        }
      }
    }
    """
    variables = {"categorySlug": "", "skip": 0, "limit": count, "filters": {}}

    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        print(response.status_code)
        raise ConnectionError

    json = response.json()
    return json["data"]["questionList"]["data"]


# def fetch_all_problems_content(count: int) -> dict:
#     headers = generate_headers()
#     query = """
#     query ($categorySlug: String
#     $limit: Int
#     $skip: Int
#     $filters: QuestionListFilterInput) {
#       questionList(
#         categorySlug: $categorySlug
#         limit: $limit
#         skip: $skip
#         filters: $filters
#       ) {
#         totalNum
#         data {
#           questionFrontendId,
#           content,
#         }
#       }
#     }
#     """
#     variables = {"categorySlug": "", "skip": 0, "limit": count, "filters": {}}

#     response = requests.post(
#         url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
#     )

#     if response.status_code != 200:
#         # TODO: handle 403 errors nicely
#         print(response.status_code)
#         raise ConnectionError

#     json = response.json()
#     return json["data"]["questionList"]["data"]


def fetch_all_problems_tags(count: int) -> dict:
    headers = generate_headers()
    query = """
    query ($categorySlug: String
    $limit: Int
    $skip: Int
    $filters: QuestionListFilterInput) {
      questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        totalNum
        data {
          questionFrontendId,
          topicTags {
            name
          }
        }
      }
    }
    """
    variables = {"categorySlug": "", "skip": 0, "limit": count, "filters": {}}

    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        print(response.status_code)
        raise ConnectionError

    json = response.json()
    return json["data"]["questionList"]["data"]
