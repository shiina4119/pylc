import requests
from . import generate_headers, GRAPHQL_URL


def fetch_snippets(title_slug: str) -> dict:
    headers = generate_headers()
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
    variables = {"titleSlug": title_slug}
    response = requests.post(
        url=GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    snippet_data = json["data"]["question"]["codeSnippets"]
    snippets = {}
    for snippet_map in snippet_data:
        snippets[snippet_map["langSlug"]] = snippet_map["code"]

    return snippets
