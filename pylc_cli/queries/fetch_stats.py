from gql import Client, gql
from . import transport


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
