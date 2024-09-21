from gql import Client, gql

from . import transport


# GraphQL queries related to problem contents
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
        result["activeDailyCodingChallengeQuestion"]["question"]["questionFrontendId"]
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


# GraphQL queries related to user data
async def fetch_user_data() -> dict:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query {
              userStatus {
                isPremium
                username
              }
            }
            """
        )

        result = await session.execute(document=query)

    return result["userStatus"]


async def fetch_user_stats() -> dict:
    user = await fetch_user_data()

    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($username: String!) {
              allQuestionsCount {
                difficulty
                count
              }
              matchedUser(username: $username) {
                submitStats {
                  acSubmissionNum {
                    difficulty
                    count
                  }
                }
              }
            }
            """
        )
        variables = {"username": user["username"]}

        result = await session.execute(document=query, variable_values=variables)

    return result


# GraphQL queries for caching
async def fetch_all_problems_count() -> int:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query {
              allQuestionsCount {
                count
              }
            }
            """
        )

        result = await session.execute(document=query)

    return result["allQuestionsCount"][0]["count"]


async def fetch_all_problems_metadata(count: int) -> dict:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($categorySlug: String
            $limit: Int
            $skip: Int
            $filters: QuestionListFilterInput) {
              questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
              ) {
                totalNum
                data {
                  questionFrontendId,
                  questionId,
                  title,
                  titleSlug,
                  difficulty,
                  isPaidOnly,
                }
              }
            }
            """
        )
        variables = {"categorySlug": "", "skip": 0, "limit": count, "filters": {}}

        result = await session.execute(document=query, variable_values=variables)

    return result["questionList"]["data"]


async def fetch_all_problems_tags(count: int) -> dict:
    async with Client(transport=transport) as session:
        query = gql(
            """
            query ($categorySlug: String
            $limit: Int
            $skip: Int
            $filters: QuestionListFilterInput) {
              questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
              ) {
                totalNum
                data {
                  questionFrontendId,
                  topicTags {
                    name
                  }
                }
              }
            }
            """
        )
        variables = {"categorySlug": "", "skip": 0, "limit": count, "filters": {}}

        result = await session.execute(document=query, variable_values=variables)

    return result["questionList"]["data"]
