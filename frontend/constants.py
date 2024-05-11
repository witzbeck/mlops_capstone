from os import getenv
from pathlib import Path

PROJECT_PATH = Path(__file__).parent

ASSETS_PATH = PROJECT_PATH / "assets"
PAGES_PATH = PROJECT_PATH / "pages"
FRONTEND_PATH = PROJECT_PATH / "frontend"
STORE_PATH = PROJECT_PATH / "store"
OUTPUTS_PATH = STORE_PATH / "outputs"
TRAINING_DATA_PATH = STORE_PATH / "datasets/robot_maintenance/train.pkl"
MLFLOW_TRACKING_URI = getenv("MLFLOW_TRACKING_URI")

APP_URL_BASE = getenv("APP_URL_BASE", "http://localhost:80")
