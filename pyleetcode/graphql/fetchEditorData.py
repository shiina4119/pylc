import requests
from pyleetcode.globals import generateHeaders, gqlUrl


def fetchEditorData(titleSlug: str) -> str:
    headers = generateHeaders(titleSlug)
    query = """
    query questionEditorData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        codeSnippets {
          langSlug
          code
        }
      }
    }       
    """
    variables = {"titleSlug": titleSlug}
    response = requests.post(
        url=gqlUrl, json={"query": query, "variables": variables}, headers=headers
    )
    rawData = response.json()
    return rawData["data"]["question"]["codeSnippets"]


if __name__ == "__main__":
    fetchEditorData("container-with-most-water")
