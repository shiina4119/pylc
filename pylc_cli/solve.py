from pathlib import Path
import subprocess
from . import BASE_DIR, EXT_MAP, con
from .queries.fetch_problem import fetch_problem_snippets


def solve(id: int, lang: str, editor: str, editor_args: list[str]):
    res = con.execute(f"SELECT title_slug FROM metadata WHERE frontend_id = {id}")
    data = res.fetchone()

    title_slug = data["title_slug"]

    file_path = Path(f"{BASE_DIR}/code/{id}.{title_slug}.{lang}.{EXT_MAP[lang]}")

    if not Path(file_path).is_file():
        file_path.touch()
        snippet = fetch_problem_snippets(title_slug=title_slug)[lang]
        file_path.write_text(snippet)

    subprocess.run([editor, *editor_args, file_path.absolute()])
