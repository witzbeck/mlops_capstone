from logging import DEBUG, basicConfig, getLogger
from os import getenv
from pathlib import Path
from warnings import filterwarnings

from pydantic import ConfigDict

log_config = basicConfig(level=DEBUG)
logger = getLogger(__name__)
filterwarnings("ignore")

from pydantic import ConfigDict

MLFLOW_TRACKING_URI = getenv("MLFLOW_TRACKING_URI")
MODULE_PATH = Path(__file__).parent
APP_ROOT = MODULE_PATH.parent
PROJECT_PATH = APP_ROOT.parent

STORE_PATH = PROJECT_PATH / "store"
if not STORE_PATH.exists():
    raise FileNotFoundError(f"Missing store directory at {STORE_PATH}")

DOCSTORE_PATH = STORE_PATH / "documents"
if not DOCSTORE_PATH.exists():
    raise FileNotFoundError(f"Missing documents directory at {DOCSTORE_PATH}")


TEMPLATE_PATH = STORE_PATH / "templates"
if not TEMPLATE_PATH.exists():
    raise FileNotFoundError(f"Missing templates directory at {TEMPLATE_PATH}")


(MODEL_STORE_PATH := STORE_PATH / "models").mkdir(exist_ok=True, parents=True)
(DATASET_STORE_PATH := STORE_PATH / "datasets").mkdir(exist_ok=True, parents=True)
(OUTPUT_STORE_PATH := STORE_PATH / "outputs").mkdir(exist_ok=True, parents=True)

# Declare no protected namespaces so that "model" can be used as a field name
config = ConfigDict(protected_namespaces=())

logger.info(f"Store Path: {STORE_PATH}")
logger.info(f"Model Store Path: {MODEL_STORE_PATH}")
logger.info(f"Dataset Store Path: {DATASET_STORE_PATH}")
logger.info(f"Output Store Path: {OUTPUT_STORE_PATH}")

if __name__ == "__main__":
    for path in (DOCSTORE_PATH).iterdir():
        print(path)
