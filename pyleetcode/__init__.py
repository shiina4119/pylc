from pathlib import Path
from rich.console import Console
import tomllib

BASE_DIR = f"{Path.home()}/.pyleetcode"
Path(f"{BASE_DIR}/code").mkdir(parents=True, exist_ok=True)

config_path = Path(f"{BASE_DIR}/config.toml")
if not config_path.is_file():
    # TODO: handle config.toml generation
    raise FileNotFoundError

with open(config_path, "rb") as f:
    data = tomllib.load(f)
    cookies = data["cookies"]
    prefs = data["preferences"]
    # TODO: handle error case for missing keys

console = Console()
