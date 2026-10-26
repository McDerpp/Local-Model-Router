import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.toml"


def load_config() -> dict:
    with CONFIG_PATH.open("rb") as file:
        return tomllib.load(file)


config = load_config()