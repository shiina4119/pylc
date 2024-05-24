import requests
from globals import gqlUrl, generateHeaders
from fetchUserData import fetchUserData


def fetchUserStats() -> dict:
    headers = generateHeaders()
    user = fetchUserData()
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
    # TODO: handle error
    variables = {"username": user["username"]}
    response = requests.post(
        url=gqlUrl,
        json={"query": query, "variables": variables},
        headers=headers,
    )
    data = response.json()
    return data


if __name__ == "__main__":
    print(fetchUserStats())
