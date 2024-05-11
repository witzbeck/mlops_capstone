from multiprocessing import Pool, set_start_method
from pathlib import Path

from pdf2image import convert_from_path
from pdfplumber import open as open_pdf
from pytesseract import image_to_string


def extract_pdf_data(pdf_path: Path) -> str:
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


def ocr_pdf_data(pdf_path: Path) -> str:
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
    # Enhanced logic to compare based on non-empty content
    if result1 and result2:
        return max(result1, result2, key=len)
    return result1 or result2


def process_pdf(pdf_path: str, use_multiprocessing=True) -> str:
    if use_multiprocessing:
        set_start_method("forkserver")
        with Pool(processes=2) as pool:
            tasks = [
                pool.apply_async(extract_pdf_data, (pdf_path,)),
                pool.apply_async(ocr_pdf_data, (pdf_path,)),
            ]
            results = [task.get() for task in tasks]  # Collect results
            best_result = compare_results(*results)
            return best_result
    else:
        # Run sequentially in the same process
        results = [extract_pdf_data(pdf_path), ocr_pdf_data(pdf_path)]
        return compare_results(*results)


if __name__ == "__main__":
    pdf_path = "path_to_your_pdf.pdf"
    try:
        best_data = process_pdf(pdf_path)
        print(best_data)
    except Exception as e:
        print(f"Error processing PDF: {e}")
