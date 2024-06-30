from pathlib import Path
import subprocess
from . import BASE_DIR, EXT_MAP, dbcon, console
from .queries.fetch_problem import fetch_problem_snippets


def solve(id: int, lang: str, editor: str, editor_args: list[str]) -> None:
    res = dbcon.execute(f"SELECT title_slug FROM metadata WHERE frontend_id = {id}")
    data = res.fetchone()

    title_slug = data["title_slug"]

    file_path = Path(f"{BASE_DIR}/code/{id}.{title_slug}.{lang}.{EXT_MAP[lang]}")

    if not Path(file_path).is_file():
        file_path.touch()
        with console.status(status="Fetching snippet...", spinner="monkey"):
            snippet = fetch_problem_snippets(title_slug=title_slug)[lang]

        file_path.write_text(snippet)

    subprocess.run([editor, *editor_args, file_path.absolute()])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    parser.add_argument("lang", choices=EXT_MAP.keys())
    parser.add_argument("editor")
    args = parser.parse_args()

    solve(args.titleslug, args.lang, args.test, [])
