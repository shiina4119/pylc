from .. import cookies


BASE_URL = "https://leetcode.com"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

def generate_headers() -> dict:
    return {
        "content-type": "application/json",
        "Origin": BASE_URL,
        "x-csrftoken": cookies["csrftoken"],
        "Cookie": \
            f"LEETCODE_SESSION={cookies["session"]}; csrftoken={cookies["csrftoken"]}"
    }
