"""
Module to train and prediction using XGBoost Classifier
"""
# !/usr/bin/env python
# coding: utf-8

from json import load
from logging import DEBUG, basicConfig, getLogger
from os import getenv, makedirs
from pathlib import Path
from sys import exit
from warnings import filterwarnings

from joblib import dump
from mlflow import (
    create_experiment,
    log_artifact,
    log_metrics,
    set_experiment,
    set_tracking_uri,
    start_run,
)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sklearn.model_selection import train_test_split

from app.extract import PDFExtractor
from app.__init__ import MLFLOW_TRACKING_URI

STORE_PATH = Path("/app/store")
OUTPUTS_PATH = STORE_PATH / "outputs"
TRAINING_DATA_PATH = STORE_PATH / "training_data"

basicConfig(level=DEBUG)
logger = getLogger(__name__)
filterwarnings("ignore")


# Constants
NUM_PDFS = 100

# Setup MLflow
set_tracking_uri(getenv("MLFLOW_TRACKING_URI"))
set_experiment("PDF_Model_Training")


# Function to generate PDFs and their expected outputs
def generate_pdfs(
    num_pdfs: int,
    output_dir: Path = TRAINING_DATA_PATH,
) -> list[tuple[str, str]]:
    makedirs(output_dir, exist_ok=True)
    data_pairs = []

    for i in range(num_pdfs):
        pdf_path = f"{output_dir}/doc_{i}.pdf"
        json_path = f"{output_dir}/doc_{i}.json"

        # Simulate structured data for PDF content
        content = {"title": f"Document {i}", "section": f"Content of document {i}"}
        expected_output = {
            "title": content["title"],
            "content": content["section"],
            "summary": f"This is a summary of document {i}.",
        }

        # Create a PDF file using ReportLab
        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, 750, content["title"])  # Positioning text at x=72, y=750
        pdf.drawString(72, 730, content["section"])  # Positioning text at x=72, y=730
        pdf.save()

        # Write the expected output
        with open(json_path, "w") as f:
            dump(expected_output, f)

        data_pairs.append((pdf_path, json_path))

    return data_pairs


class PDFExtraction:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.file = None
        self.y_train = None
        self.y_test = None
        self.X_train_scaled_transformed = None
        self.X_test_scaled_transformed = None
        self.accuracy_scr = None
        self.model_path = None
        self.parameters = None
        self.robust_scaler = None
        self.run_id = None
        self.active_experiment = None
        self.vision_model = None

    def mlflow_tracking(
        self,
        tracking_uri: str = MLFLOW_TRACKING_URI,
        experiment: str = None,
        new_experiment: str = None,
    ):
        # sets tracking URI
        set_tracking_uri(tracking_uri)

        # creates new experiment if no experiment is specified
        if experiment is None:
            create_experiment(new_experiment)
            self.active_experiment = new_experiment
            set_experiment(new_experiment)
        else:
            set_experiment(experiment)
            self.active_experiment = experiment

    def train(self, data_pairs: list[tuple[str, str]]):
        """trains the model and logs the model as mlflow artifact

        Parameters
        ----------
        ncpu : int, optional
            number of CPU threads used for training, by default 4
        """
        train_data, val_data = train_test_split(
            data_pairs, test_size=0.2, random_state=42
        )

        extractor = PDFExtractor(MLFLOW_TRACKING_URI)

        for phase, data in [("train", train_data), ("validation", val_data)]:
            with start_run():
                for pdf_path, json_path in data:
                    logger.info(f"Extracting {phase} data using the PDFExtractor")
                    extracted_data = extractor.extract_data(pdf_path, input_type="file")

                    # Read the expected data
                    with open(json_path, "r") as f:
                        expected_data = load(f)

                    # Calculate performance metrics (e.g., accuracy)
                    accuracy = sum(
                        1
                        for key in extracted_data
                        if extracted_data.get(key) == expected_data.get(key)
                    ) / len(expected_data)

                    # Log to MLflow
                    log_metrics({"accuracy": accuracy})

                    print(f"Processed {pdf_path}: Accuracy = {accuracy}")

    def validate(self):
        """performs model validation with testing data

        Returns
        -------
        float
            accuracy metric
        """
        logger.info("Validating model")
        self.accuracy_scr = self.vision_model.score(
            self.X_test_scaled_transformed, self.y_test
        )
        logger.info(f"Accuracy: {self.accuracy_scr}")
        return self.accuracy_scr

    def save(self, model_path):
        """Logs scaler as mlflow artifact.

        Parameters
        ----------
        model_path : str
            path where trained model should be saved
        """

        self.scaler_path = model_path + self.model_name + "_scaler.joblib"

        logger.info("Saving Scaler")
        with open(self.scaler_path, "wb") as fh:
            dump(self.robust_scaler, fh.name)

        logger.info("Saving Scaler as MLFLow Artifact")
        with start_run(self.run_id):
            log_artifact(self.scaler_path)


if __name__ == "__main__":
    data_pairs = generate_pdfs(NUM_PDFS)
    extractor = PDFExtraction("PDFExtraction")
    extractor.mlflow_tracking(MLFLOW_TRACKING_URI)
    extractor.train(data_pairs)
    logger.info("Training completed successfully")
    exit(0)
