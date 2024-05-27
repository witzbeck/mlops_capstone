"""This module contains the inference function that is used to make predictions on new data samples."""

from mlflow import pyfunc
from mlflow.artifacts import download_artifacts

from app.__init__ import getLogger

logger = getLogger(__name__)


def inference(
    model_name: str,
    stage: str,
    model_run_id: int,
    scaler_file_name: str,
    scaler_destination: str,
    data: str,
):
    # retrieve scaler
    download_artifacts(
        run_id=model_run_id, artifact_path=scaler_file_name, dst_path=scaler_destination
    )

    # load model
    model = pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")
    return model
