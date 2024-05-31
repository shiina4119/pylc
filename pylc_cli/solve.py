from pathlib import Path
import tomllib
import subprocess
from . import BASE_DIR, EXT_MAP
from .queries.fetch_question import fetch_question
from .queries.fetch_snippets import fetch_snippets


def solve(title_slug: str, lang: str, editor: str, editor_args: list[str]):
    question = fetch_question(title_slug=title_slug)
    id = question["questionFrontendId"]

    file_path = Path(f"{BASE_DIR}/code/{id}.{title_slug}.{lang}.{EXT_MAP[lang]}")

    if not Path(file_path).is_file():
        file_path.touch()
        snippet = fetch_snippets(title_slug=title_slug)[lang]
        file_path.write_text(snippet)

    subprocess.run([editor, *editor_args, file_path.absolute()])
