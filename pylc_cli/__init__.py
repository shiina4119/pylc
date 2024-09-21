import sqlite3
from pathlib import Path

import tomli_w
import tomllib
from rich.console import Console

BASE_DIR = f"{Path.home()}/.pylc"
CACHE_PATH = f"{BASE_DIR}/cache.sqlite"

EXT_MAP = {
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "python": "py",
    "python3": "py",
    "csharp": "cs",
    "javascript": "js",
    "typescript": "ts",
    "php": "php",
    "swift": "swift",
    "kotlin": "kt",
    "dart": "dart",
    "golang": "go",
    "ruby": "rb",
    "scala": "scala",
    "rust": "rs",
    "racket": "rkt",
    "erlang": "erl",
    "elixir": "exs",
}

Path(f"{BASE_DIR}/code").mkdir(parents=True, exist_ok=True)

dbcon = sqlite3.connect(CACHE_PATH)
dbcon.row_factory = sqlite3.Row

console = Console()
err_console = Console(stderr=True)

config_path = Path(f"{BASE_DIR}/config.toml")
if not config_path.is_file():
    err_console.print("config.toml not found. Generating a new one...")
    err_console.print("Paste your cookies in the new config.toml file.")
    config_path.touch()

    default_config = {
        "preferences": {
            "lang": "python3",
            "editor": "vi",
            "editor_args": [],
            "tags": True,
        },
        "cookies": {"csrftoken": "", "session": ""},
    }

    with config_path.open("wb") as f:
        tomli_w.dump(default_config, f)

with open(config_path, "rb") as f:
    data = tomllib.load(f)
    cookies = data["cookies"]
    prefs = data["preferences"]
    # TODO: handle error case for missing keys


inject_path = Path(f"{BASE_DIR}/inject.toml")
if not inject_path.is_file():
    inject_path.touch()
    lang_keys = {}
    for lang in EXT_MAP.keys():
        lang_keys[lang] = {}

    with inject_path.open("wb") as f:
        tomli_w.dump(lang_keys, f)

with inject_path.open("rb") as f:
    inject = tomllib.load(f)
