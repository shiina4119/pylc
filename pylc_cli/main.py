import argparse
from . import EXT_MAP, prefs
from .display_problem import display_problem
from .run_solution import run
from .solve import solve
from .cache import update_cache
from .queries.fetch_problem import fetch_daily


def main():
    lang = prefs["lang"]
    editor = prefs["editor"]
    editor_args = prefs["editor_args"]

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    daily_parser = subparsers.add_parser("daily")

    pick_parser = subparsers.add_parser("pick")
    pick_parser.add_argument("id", type=int)

    solve_parser = subparsers.add_parser("solve")
    solve_parser.add_argument("id", type=int)
    solve_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("id", type=int)
    test_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    submit_parser = subparsers.add_parser("submit")
    submit_parser.add_argument("id", type=int)
    submit_parser.add_argument("--lang", default=lang, choices=EXT_MAP.keys())

    update_parser = subparsers.add_parser("update")

    args = parser.parse_args()

    if args.command == "daily":
        display_problem(id=fetch_daily())

    if args.command == "pick":
        display_problem(id=args.id)

    elif args.command == "solve":
        solve(
            id=args.id,
            lang=args.lang,
            editor=editor,
            editor_args=editor_args,
        )

    elif args.command == "test":
        run(id=args.id, lang=args.lang, test=True)

    elif args.command == "submit":
        run(id=args.id, lang=args.lang, test=False)

    elif args.command == "update":
        update_cache()
