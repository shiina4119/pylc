import argparse
from pathlib import Path
from . import BASE_DIR, EXT_MAP, prefs
from .display_question import display_question
from .run_solution import run
from .solve import solve
from .queries.fetch_question import fetch_daily


def main():
    lang = prefs["lang"]
    editor = prefs["editor"]
    editor_args = prefs["editor_args"]

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    daily_parser = subparsers.add_parser("daily")

    pick_parser = subparsers.add_parser("pick")
    pick_parser.add_argument("titleslug")

    solve_parser = subparsers.add_parser("solve")
    solve_parser.add_argument("titleslug")
    solve_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("titleslug")
    test_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    submit_parser = subparsers.add_parser("submit")
    submit_parser.add_argument("titleslug")
    submit_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    args = parser.parse_args()

    if args.command == "daily":
        display_question(title_slug=fetch_daily())

    if args.command == "pick":
        display_question(title_slug=args.titleslug)

    elif args.command == "solve":
        solve(
            title_slug=args.titleslug,
            lang=args.lang,
            editor=editor,
            editor_args=editor_args,
        )

    elif args.command == "test":
        run(title_slug=args.titleslug, lang=args.lang, test=True)

    elif args.command == "submit":
        run(title_slug=args.titleslug, lang=args.lang, test=False)
