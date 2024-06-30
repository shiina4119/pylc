from . import app, EXT_MAP, prefs
from .cache import update_cache
from .display_problem import display_problem
from .queries.fetch_problem import fetch_daily
from .run_solution import run_solution
from .solve_problem import solve_problem

lang = prefs["lang"]
editor = prefs["editor"]
editor_args = prefs["editor_args"]


@app.command()
def daily() -> None:
    display_problem(id=fetch_daily())


@app.command()
def pick(id: int = fetch_daily()) -> None:
    display_problem(id=id)


@app.command()
def solve(id: int, lang: str = lang) -> None:
    solve_problem(id=id, lang=lang, editor=editor, editor_args=editor_args)


@app.command()
def test(id: int, lang: str = lang) -> None:
    run_solution(id=id, lang=lang, test=True)


@app.command()
def submit(id: int, lang: str = lang) -> None:
    run_solution(id=id, lang=lang, test=False)


@app.command()
def update() -> None:
    update_cache()


def main():
    app()


if __name__ == "__main__":
    main()
