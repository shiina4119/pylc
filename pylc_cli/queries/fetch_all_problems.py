from gql import Client, gql
from . import headers, transport


async def fetch_all_problems_count() -> int:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query {
              allQuestionsCount {
                count
              }
            }
            """
        )
    response = requests.post(url=GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    count = json["data"]["allQuestionsCount"][0]["count"]
    return count


def fetch_all_problems_metadata(count: int) -> dict:
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


def fetch_all_problems_tags(count: int) -> dict:
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
