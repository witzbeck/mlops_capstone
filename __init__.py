from os import environ
from pathlib import Path

PROJECT_PATH = Path(__file__).parent
dotenv_file = PROJECT_PATH / ".env"
if not dotenv_file.exists():
    raise FileNotFoundError(f"Missing .env file at {dotenv_file}")

env_lines = [
    line.strip()
    for line in dotenv_file.read_text().splitlines()
    if line.strip() and not line.strip().startswith("#")
]
pairs = {k: v for k, v in (line.split("=", 1) for line in env_lines)}
environ.update(pairs)

STORE_PATH = PROJECT_PATH / "store"
if not STORE_PATH.exists():
    raise FileNotFoundError(f"Missing store directory at {STORE_PATH}")

(models := STORE_PATH / "models").mkdir(exist_ok=True, parents=True)
(datasets := STORE_PATH / "datasets").mkdir(exist_ok=True, parents=True)
(outputs := STORE_PATH / "outputs").mkdir(exist_ok=True, parents=True)


DOCSTORE_PATH = STORE_PATH / "documents"
if not DOCSTORE_PATH.exists():
    raise FileNotFoundError(f"Missing documents directory at {DOCSTORE_PATH}")

if __name__ == "__main__":
    for path in (DOCSTORE_PATH).iterdir():
        print(path)
