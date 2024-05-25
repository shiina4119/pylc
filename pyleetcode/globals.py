from os.path import exists, expanduser
import tomllib
from importlib import resources as rs

baseUrl = "https://leetcode.com"
gqlUrl = f"{baseUrl}/graphql"

def runUrl(titleSlug: str, test: bool = True) -> str:
    url = f"{baseUrl}/problems/{titleSlug}"
    # TODO: handle error for bad titleSlug
    if test:
        url += "/interpret_solution/"
    else:
        url += "/submit/"

    return url

def readConfig(key) -> dict:
    path = f"{expanduser("~")}/.pyleetcode"
    if not exists(f"{path}/config.toml"):
        # TODO: handle config.toml generation
        raise FileNotFoundError

    with open(f"{path}/config.toml", "rb") as f:
        rawData = tomllib.load(f)
        data = rawData[key]
        # key can be "cookies" or "preferences"
        # TODO: write error handling code for when cookies are not present

    return data

def readSourceCode(questionId: str, titleSlug: str, lang: str) -> str:
    langFile = rs.files() / "lang.toml"
    with langFile.open("rb") as f:
        langMap = tomllib.load(f)

    fileName = f"{questionId}.{titleSlug}.{langMap[lang]}"
    path = f"{expanduser("~")}/.pyleetcode/code/{fileName}"

    if not exists(path):
        # TODO: tell user to write code first
        raise FileNotFoundError

    with open(path, "r") as f:
        lines = f.readlines()

    codeString = "".join(lines)
    return codeString

def generateHeaders(referer: str = "") -> dict:
    headers = {
        "content-type": "application/json",
        "Origin": "https://leetcode.com"
    }
    cookies = readConfig("cookies")

    if referer:
        headers["Referer"] = f"{baseUrl}/{referer}"

    headers["x-csrftoken"] = cookies["csrftoken"]
    headers["Cookie"] = \
        f"LEETCODE_SESSION={cookies["session"]}; csrftoken={cookies["csrftoken"]}"

    return headers

if __name__ == "__main__":
    print(generateHeaders())
