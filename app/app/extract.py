from multiprocessing import Pool
from pathlib import Path

from pytesseract import image_to_string
from pdf2image import convert_from_path
from pdfplumber import open as open_pdf


def extract_pdf_data(pdf_path):
    try:
        with open_pdf(pdf_path) as pdf:
            # Use list comprehension for efficient text accumulation
            text = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "".join(text)  # Join list into a single string
    except Exception as e:
        raise RuntimeError("Error in PDF extraction") from e


def ocr_pdf_data(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        # Utilize comprehension and join directly to avoid intermediate list storage
        text = " ".join(image_to_string(image) for image in images)
        return text
    except Exception as e:
        raise RuntimeError("Error in OCR process") from e


def compare_results(result1, result2):
    # Enhanced logic to compare based on non-empty content
    if result1 and result2:
        return max(result1, result2, key=len)
    return result1 or result2


def process_pdf(pdf_path: Path) -> dict[str, str]:
    # Properly utilize multiprocessing to handle different tasks
    with Pool(processes=2) as pool:
        # Setup tasks and retrieve results
        tasks = [
            pool.apply_async(extract_pdf_data, (pdf_path,)),
            pool.apply_async(ocr_pdf_data, (pdf_path,)),
        ]
        results = [task.get() for task in tasks]  # Collect results
        best_result = compare_results(*results)
        return best_result


# Usage
pdf_path = "path_to_your_pdf.pdf"
try:
    best_data = process_pdf(pdf_path)
    print(best_data)
except Exception as e:
    print(f"Error processing PDF: {e}")
