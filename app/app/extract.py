from base64 import b64decode
from io import BytesIO
from json import dumps
from multiprocessing import Pool, set_start_method
from pathlib import Path

from mlflow import log_artifact, log_param, set_experiment, set_tracking_uri, start_run
from pdf2image import convert_from_bytes, convert_from_path
from pdfplumber import open as open_pdf
from pytesseract import image_to_string
from requests import get

from app.__init__ import getLogger

logger = getLogger(__name__)


def extract_pdf_data(pdf_path: Path) -> str:
    """extracts text from PDF file using pdfplumber"""
    logger.info(f"Extracting text from PDF: {pdf_path}")
    try:
        with open_pdf(pdf_path) as pdf:
            text = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "".join(text)
    except FileNotFoundError as e:
        raise RuntimeError(f"PDF file not found: {pdf_path}\n{e}") from e
    except IOError as e:
        raise RuntimeError(f"Error reading PDF file: {pdf_path}\n{e}") from e
    except Exception as e:
        raise RuntimeError(f"Error in PDF extraction from {pdf_path}\n{e}") from e


def extract_ocr_data(pdf_path: Path) -> str:
    """extracts text from PDF file using OCR"""
    logger.info(f"Extracting text from PDF using OCR: {pdf_path}")
    try:
        images = convert_from_path(pdf_path)
        # Utilize comprehension and join directly to avoid intermediate list storage
        text = " ".join(image_to_string(image) for image in images)
        return text
    except IOError as e:
        raise RuntimeError(f"Error reading PDF file: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error in OCR process: {e}") from e


def compare_results(
    result1: str,
    result2: str,
) -> str:
    """Compares two results and returns the one with the most content"""
    logger.info("Comparing results")
    if result1 and result2:
        return max(result1, result2, key=len)
    return result1 or result2


def process_pdf(pdf_path: Path, use_multiprocessing=True) -> str:
    """Extracts text from PDF using pdfplumber and OCR, then compares the results"""
    logger.info(f"Processing PDF: {pdf_path}")
    if isinstance(pdf_path, bytes):
        return convert_from_bytes(pdf_path, single_file=True)[0]
    if isinstance(pdf_path, str):
        pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if use_multiprocessing:
        set_start_method("forkserver")
        with Pool(processes=2) as pool:
            tasks = [
                pool.apply_async(extract_pdf_data, (pdf_path,)),
                pool.apply_async(extract_ocr_data, (pdf_path,)),
            ]
            results = [task.get() for task in tasks]  # Collect results
            best_result = compare_results(*results)
            return best_result
    else:
        # Run sequentially in the same process
        results = [extract_pdf_data(pdf_path), extract_ocr_data(pdf_path)]
        return compare_results(*results)


class PDFExtractor:
    def __init__(self, mlflow_tracking_uri: str):
        logger.info(
            f"Setting up PDFExtractor with MLFlow tracking URI: {mlflow_tracking_uri}"
        )
        set_tracking_uri(mlflow_tracking_uri)
        set_experiment("PDF_Extraction")

    def read_pdf_from_file(self, filepath):
        with open(filepath, "rb") as file:
            return self.process_pdf(file)

    def read_pdf_from_base64(self, base64_data):
        pdf_bytes = b64decode(base64_data)
        return self.process_pdf(BytesIO(pdf_bytes))

    def read_pdf_from_url(self, url):
        response = get(url)
        response.raise_for_status()
        return self.process_pdf(BytesIO(response.content))

    def structure_data(self, raw_text):
        # This method should be implemented to structure raw text into a dictionary
        # based on your specific data structuring needs.
        structured_data = {"content": raw_text}
        return structured_data

    def validate_data(self, data):
        # Implement validation logic
        # This could be as simple as checking data types, or as complex as applying a schema validation
        return True

    def pass_to_llm(self, structured_data):
        # Code to pass structured data to an LLM and get the processed output
        # This could involve calling an API or using a direct library method
        processed_data = structured_data  # Placeholder for actual LLM processing
        return processed_data

    def extract_data(self, input_data, input_type="file"):
        with start_run():
            if input_type == "file":
                raw_text = self.read_pdf_from_file(input_data)
            elif input_type == "base64":
                raw_text = self.read_pdf_from_base64(input_data)
            elif input_type == "url":
                raw_text = self.read_pdf_from_url(input_data)
            else:
                raise ValueError("Unsupported input type")

            structured_data = self.structure_data(raw_text)
            if self.validate_data(structured_data):
                final_data = self.pass_to_llm(structured_data)
                log_param("input_type", input_type)
                log_artifact(dumps(final_data), "output.json")
                return final_data
            else:
                raise ValueError("Data validation failed")


if __name__ == "__main__":
    pdf_path = "path_to_your_pdf.pdf"
    try:
        best_data = process_pdf(pdf_path)
        print(best_data)
    except Exception as e:
        print(f"Error processing PDF: {e}")
