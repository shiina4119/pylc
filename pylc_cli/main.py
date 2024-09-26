import asyncio

import typer
from typing_extensions import Annotated

from . import EXT_MAP, config_path, err_console, prefs
from .cache import update_cache
from .display_problem import display_problem
from .queries.graphql import fetch_daily
from .run_solution import run_solution
from .solve_problem import solve_problem

prefs_lang = prefs["lang"]
prefs_editor = prefs["editor"]
prefs_editor_args = prefs["editor_args"]

app = typer.Typer(no_args_is_help=True, help="Solve leetcode problems from the CLI!")


@app.command()
def daily() -> None:
    """
    Display problem statement of daily problem.
    """
    daily_id = asyncio.run(fetch_daily())
    asyncio.run(display_problem(id=daily_id))


@app.command()
def pick(
    typer_argument_id: Annotated[int, typer.Argument("id", help="Problem ID")],
) -> None:
    """
    Display problem statement.
    """
    asyncio.run(display_problem(id=typer_argument_id))


@app.command()
def solve(
    typer_argument_id: Annotated[int, typer.Argument("id", help="Problem ID")],
    typer_option_lang: Annotated[
        str, typer.Option("--lang", help="Choose language")
    ] = prefs_lang,
) -> None:
    """
    Open problem in editor.
    Pass --lang <lang> to select a different language.
    """
    if typer_option_lang not in EXT_MAP:
        err_console.print("Cannot use this language.")

    asyncio.run(
        solve_problem(
            id=typer_argument_id,
            lang=typer_option_lang,
            editor=prefs_editor,
            editor_args=prefs_editor_args,
        )
    )


@app.command()
def test(
    typer_argument_id: Annotated[int, typer.Argument("id", help="Problem ID")],
    typer_option_lang: Annotated[
        str, typer.Option("--lang", help="Choose language")
    ] = prefs_lang,
) -> None:
    """
    Send problem to leetcode servers for testing.
    Pass --lang <lang> to select a different language.
    """
    if typer_option_lang not in EXT_MAP:
        err_console.print("Cannot use this language.")

    asyncio.run(run_solution(id=typer_argument_id, lang=typer_option_lang, test=True))


@app.command()
def submit(
    typer_argument_id: Annotated[int, typer.Argument("id", help="Problem ID")],
    typer_option_lang: Annotated[
        str, typer.Option("--lang", help="Choose language")
    ] = prefs_lang,
) -> None:
    """
    Submit problem.
    Pass --lang <lang> to select a different language.
    """
    if typer_option_lang not in EXT_MAP:
        err_console.print("Cannot use this language.")

    asyncio.run(run_solution(id=typer_argument_id, lang=typer_option_lang, test=False))


@app.command()
def update() -> None:
    """
    Build problem cache. Run this once after installing the package.
    """
    asyncio.run(update_cache())


@app.command()
def config() -> None:
    """
    Open your configuration file.
    """
    import subprocess

    subprocess.run([prefs_editor, *prefs_editor_args, config_path.absolute()])


def main():
    app()


if __name__ == "__main__":
    main()
