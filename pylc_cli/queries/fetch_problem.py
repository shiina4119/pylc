from gql import Client, gql
from . import transport


async def fetch_daily() -> int:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query {
              activeDailyCodingChallengeQuestion {
                question {
                  questionFrontendId
                }
              }
            }
            """
        )

        result = await session.execute(document=query)
        return int(
            result["activeDailyCodingChallengeQuestion"]["question"][
                "questionFrontendId"
            ]
        )


async def fetch_problem_content(title_slug: str) -> str:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                content
              }
            }
            """
        )
        variables = {"titleSlug": title_slug}

        result = await session.execute(document=query, variable_values=variables)
        return result["question"]["content"]


async def fetch_problem_snippets(title_slug: str) -> dict:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                codeSnippets {
                  langSlug
                  code
                }
              }
            }
            """
        )
        variables = {"titleSlug": title_slug}

        result = await session.execute(document=query, variable_values=variables)
        snippets = {
            snippet_map["langSlug"]: snippet_map["code"]
            for snippet_map in result["question"]["codeSnippets"]
        }
        return snippets


async def fetch_problem_testcases(title_slug: str) -> str:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                exampleTestcaseList
              }
            }
            """
        )
        variables = {"titleSlug": title_slug}

        result = await session.execute(document=query, variable_values=variables)
        return result["question"]["exampleTestcaseList"]
