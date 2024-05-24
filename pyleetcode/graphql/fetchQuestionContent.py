import requests
from globals import gqlUrl, generateHeaders


def fetchQuestionContent(titleSlug: str) -> dict:
    # TODO: fetch question using question_id
    headers = generateHeaders()
    query = """
    query ($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        content
        mysqlSchemas
        exampleTestcaseList
        topicTags {
          name
        }
      }
    }
    """
    variables = {"titleSlug": titleSlug}
    # TODO: handle error
    response = requests.post(
        url=gqlUrl, json={"query": query, "variables": variables}, headers=headers
    )
    data = response.json()
    return data["data"]["question"]


if __name__ == "__main__":
    titleSlug = input("Enter title-slug of problem: ")
    print(fetchQuestionContent(titleSlug))
