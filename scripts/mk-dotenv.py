"""writes all existing environment variable key-value pairs to a .env file
in the current working directory"""

from collections.abc import Mapping
from logging import info
from os import environ
from pathlib import Path


def dump_dotenv(path: Path | None, pairs: Mapping | None, force: bool = False) -> Path:
    if path is None:
        path = Path.cwd() / ".env"
        info(f"Path not provided, using {path}")
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists, use force=True to overwrite")
    if pairs is None:
        pairs = environ
        info("Pairs not provided, using environ")
    path.write_text("\n".join([f"{key}={value}" for key, value in pairs.items()]))
    info(f"Dumped {len(pairs)} key-value pairs to {path}")
    return path


if __name__ == "__main__":
    dump_dotenv()
