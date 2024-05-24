import requests
from globals import gqlUrl, generateHeaders


def fetchUserData() -> dict:
    headers = generateHeaders()
    query = """
    query {
      userStatus {
        isPremium
        username
      }
    }
    """
    # TODO: handle error
    response = requests.post(url=gqlUrl, json={"query": query}, headers=headers)
    data = response.json()
    return data["data"]["userStatus"]
