from pathlib import Path
import subprocess
from . import BASE_DIR, EXT_MAP, dbcon, console
from .queries.graphql import fetch_problem_snippets


async def solve_problem(
    id: int, lang: str, editor: str, editor_args: list[str]
) -> None:
    res = dbcon.execute(f"SELECT title_slug FROM metadata WHERE frontend_id = {id}")
    data = res.fetchone()

    title_slug = data["title_slug"]

    file_path = Path(f"{BASE_DIR}/code/{id}.{title_slug}.{lang}.{EXT_MAP[lang]}")

    if not Path(file_path).is_file():
        file_path.touch()
        with console.status(status="Fetching snippet...", spinner="monkey"):
            snippets = await fetch_problem_snippets(title_slug=title_slug)

        file_path.write_text(snippets[lang])

    subprocess.run([editor, *editor_args, file_path.absolute()])


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    parser.add_argument("lang", choices=EXT_MAP.keys())
    parser.add_argument("editor")
    args = parser.parse_args()

    asyncio.run(solve_problem(args.titleslug, args.lang, args.test, []))
