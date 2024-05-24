import requests
from globals import gqlUrl, generateHeaders


def fetchDailyQuestion() -> dict:
    headers = generateHeaders()
    query = """
    query {
      activeDailyCodingChallengeQuestion {
        question {
          titleSlug
        }
      }
    }
    """
    # TODO: handle error
    response = requests.post(url=gqlUrl, json={"query": query}, headers=headers)
    data = response.json()
    return data["data"]["activeDailyCodingChallengeQuestion"]["question"]


if __name__ == "__main__":
    print(fetchDailyQuestion())
