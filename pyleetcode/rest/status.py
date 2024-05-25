import requests
from run import runCode
from pyleetcode.globals import generateHeaders, statusUrl
from time import sleep


def getStatus(titleSlug: str, test: bool = True) -> dict:
    id = runCode(titleSlug=titleSlug, test=test)
    url = statusUrl(id)

    if test:
        headers = generateHeaders(f"problems/{titleSlug}/submissions")
    else:
        headers = generateHeaders(f"problems/{titleSlug}")

    while True:
        response = requests.post(url=url, headers=headers)
        sleep(0.5)
        data = response.json()
        if data["state"] == "SUCCESS":
            break

    return data


if __name__ == "__main__":
    print(getStatus("two-sum"))
