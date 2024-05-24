import os
import tomllib
from pathlib import Path

baseUrl = "https://leetcode.com"
gqlUrl = f"{baseUrl}/graphql"

def generateHeaders() -> dict:
    def __readCookies() -> dict:
        HOME = os.getenv("HOME")
        path = f"{HOME}/.pyleetcode"
        data = {}
        # TODO: seperate the logic for creating config file
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            f = open(f"{path}/config.toml", "x")
            # TODO: generate config template
        except FileExistsError:
            with open(f"{path}/config.toml", "rb") as f:
                data = tomllib.load(f)
                # TODO: write error handling code for when cookies are not present

        return data["cookies"]

    cookies = __readCookies()

    return {
        "content-type": "application/json",
        "x-csrftoken": cookies["csrftoken"],
        "Origin": baseUrl,
        "Cookie": \
            f"LEETCODE_SESSION={cookies["session"]}; csrftoken={cookies["csrftoken"]}",
    }
