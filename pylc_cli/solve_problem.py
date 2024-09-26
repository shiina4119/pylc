import subprocess
from pathlib import Path

from . import BASE_DIR, EXT_MAP, console, dbcon, inject
from .queries.graphql import fetch_problem_snippets


async def solve_problem(
    problem_id: int, lang: str, reset: bool, editor: str, editor_args: list[str]
) -> None:
    res = dbcon.execute(
        f"SELECT title_slug FROM metadata WHERE frontend_id = {problem_id}"
    )
    data = res.fetchone()

    title_slug = data["title_slug"]

    file_path = Path(
        f"{BASE_DIR}/code/{problem_id}.{title_slug}.{lang}.{EXT_MAP[lang]}"
    )

    if reset:
        Path(file_path).unlink(missing_ok=True)

    if not Path(file_path).is_file():
        file_path.touch()
        with console.status(status="Fetching snippet...", spinner="monkey"):
            snippets = await fetch_problem_snippets(title_slug=title_slug)

        with open(file_path, "a") as f:
            if (lang in inject) and ("inject_before" in inject[lang]):
                f.write("\n".join(inject[lang]["inject_before"]))
                f.write("\n\n")

            f.write(snippets[lang])

    subprocess.run([editor, *editor_args, file_path.absolute()])


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    parser.add_argument("lang", choices=EXT_MAP.keys())
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("editor")
    args = parser.parse_args()

    asyncio.run(solve_problem(args.id, args.lang, args.reset, args.test, []))
