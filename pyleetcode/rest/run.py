import requests
import json
from pyleetcode.globals import generateHeaders, runUrl, readConfig, readSourceCode
from pyleetcode.graphql.fetchQuestionContent import fetchQuestionContent


def runCode(titleSlug: str, test: bool = True):
    url = runUrl(titleSlug=titleSlug, test=test)
    headers = generateHeaders(referer=f"problems/{titleSlug}")
    questionContent = fetchQuestionContent(titleSlug=titleSlug)

    lang = readConfig("preferences")["lang"]
    questionId = questionContent["questionId"]
    typedCode = readSourceCode(questionId=questionId, titleSlug=titleSlug, lang=lang)

    payload = {
        "lang": lang,
        "question_id": questionId,
        "typed_code": typedCode,
    }

    if test:
        inputStr = ""
        for i in questionContent["exampleTestcaseList"]:
            inputStr += i + "\n"

        payload["data_input"] = inputStr

    response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    return response.json()
