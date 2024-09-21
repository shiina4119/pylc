import asyncio

import aiohttp

from . import BASE_URL, headers


async def get_status(title_slug: str, id: str, test: bool = True) -> dict:
    url = f"{BASE_URL}/submissions/detail/{id}/check/"

    headers["Referer"] = f"{BASE_URL}/problems/{title_slug}"
    if test:
        headers["Referer"] += "/submissions"

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.post(url=url, headers=headers) as response:
                _json = await response.json()
                if _json["state"] == "SUCCESS":
                    break

            await asyncio.sleep(2)

        return _json
