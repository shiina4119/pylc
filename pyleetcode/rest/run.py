import requests
import json
from pyleetcode.globals import generateHeaders, runUrl, readConfig
from pyleetcode.graphql.fetchQuestionContent import fetchQuestionContent


def runCode(titleSlug: str, test: bool = True):
    url = runUrl(titleSlug=titleSlug, test=test)
    headers = generateHeaders(referer=f"problems/{titleSlug}")

    lang = readConfig("preferences")["lang"]

    questionContent = fetchQuestionContent(titleSlug=titleSlug)

    questionId = questionContent["questionId"]

    payload = {
        "lang": lang,
        "question_id": questionId,
        # TODO: finish typed_code
        "typed_code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:    return [4]",
    }

    if test:
        inputStr = ""
        for i in questionContent["exampleTestcaseList"]:
            inputStr += i + "\n"

        payload["data_input"] = inputStr

    response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    return response.json()


if __name__ == "__main__":
    print(runCode("two-sum"))
