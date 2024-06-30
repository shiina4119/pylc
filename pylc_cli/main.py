from typing_extensions import Annotated
import typer
from . import config_path, EXT_MAP, err_console, prefs
from .cache import update_cache
from .display_problem import display_problem
from .queries.fetch_problem import fetch_daily
from .run_solution import run_solution
from .solve_problem import solve_problem

lang = prefs["lang"]
editor = prefs["editor"]
editor_args = prefs["editor_args"]

app = typer.Typer(no_args_is_help=True, help="Solve leetcode problems from the CLI!")


@app.command()
def daily() -> None:
    """
    Display problem statement of daily problem.
    """
    display_problem(id=fetch_daily())


@app.command()
def pick(id: Annotated[int, typer.Argument(help="Problem ID")] = fetch_daily()) -> None:
    """
    Display problem statement. If ID is not provided, acts the same as daily command.
    """
    display_problem(id=id)


@app.command()
def solve(
    id: Annotated[int, typer.Argument(help="Problem ID")],
    lang: Annotated[str, typer.Option(help="Choose language")] = lang,
) -> None:
    """
    Open problem in editor.
    Pass --lang <lang> to select a different language.
    """
    if lang not in EXT_MAP:
        err_console.print("Cannot use this language.")
    solve_problem(id=id, lang=lang, editor=editor, editor_args=editor_args)


@app.command()
def test(
    id: Annotated[int, typer.Argument(help="Problem ID")],
    lang: Annotated[str, typer.Option(help="Choose language")] = lang,
) -> None:
    """
    Send problem to leetcode servers for testing.
    Pass --lang <lang> to select a different language.
    """
    if lang not in EXT_MAP:
        err_console.print("Cannot use this language.")
    run_solution(id=id, lang=lang, test=True)


@app.command()
def submit(
    id: Annotated[int, typer.Argument(help="Problem ID")],
    lang: Annotated[str, typer.Option(help="Choose language")] = lang,
) -> None:
    """
    Submit problem.
    Pass --lang <lang> to select a different language.
    """
    if lang not in EXT_MAP:
        err_console.print("Cannot use this language.")
    run_solution(id=id, lang=lang, test=False)


@app.command()
def update() -> None:
    """
    Build problem cache. Run this once after installing the package.
    """
    update_cache()


@app.command()
def config() -> None:
    """
    Open your configuration file.
    """
    import subprocess

    subprocess.run([editor, *editor_args, config_path.absolute()])


def main():
    app()


if __name__ == "__main__":
    main()
