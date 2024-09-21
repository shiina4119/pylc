from gql.transport.aiohttp import AIOHTTPTransport

from .. import cookies

BASE_URL = "https://leetcode.com"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

headers = {
    "content-type": "application/json",
    "Origin": BASE_URL,
    "x-csrftoken": cookies["csrftoken"],
    "Cookie": f"LEETCODE_SESSION={cookies['session']}; csrftoken={cookies['csrftoken']}",
}

transport = AIOHTTPTransport(url=GRAPHQL_URL, headers=headers)
