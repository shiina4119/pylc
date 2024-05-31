import requests
from . import GRAPHQL_URL, generate_headers


def fetch_user_data() -> dict:
    headers = generate_headers()
    query = """
    query {
      userStatus {
        isPremium
        username
      }
    }
    """
    response = requests.post(url=GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    return json["data"]["userStatus"]


def fetch_user_stats() -> dict:
    headers = generate_headers()
    user = fetch_user_data()
    query = """
    query ($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    variables = {"username": user["username"]}
    response = requests.post(
        url=GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=headers,
    )
    if response.status_code != 200:
        # TODO: handle 403 errors nicely
        raise ConnectionError

    json = response.json()
    return json
