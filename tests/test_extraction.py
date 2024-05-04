import unittest
from unittest.mock import MagicMock, patch

from app.new import (  # Import your functions
    compare_results,
    extract_pdf_data,
    ocr_pdf_data,
    process_pdf,
)


class TestPDFProcessing(unittest.TestCase):
    
    def test_extract_pdf_data_success(self):
        # Mock pdfplumber.open to simulate PDF reading
        with patch("pdfplumber.open", MagicMock(return_value=MagicMock(pages=[MagicMock(extract_text=lambda: "This is a test.")]))) as mock_pdf:
            result = extract_pdf_data("dummy_path.pdf")
            self.assertEqual(result, "This is a test.")
            mock_pdf.assert_called_once_with("dummy_path.pdf")

    def test_extract_pdf_data_failure(self):
        # Simulate an exception during PDF reading
        with patch("pdfplumber.open", side_effect=Exception("Failed to open PDF")):
            with self.assertRaises(RuntimeError) as context:
                extract_pdf_data("faulty_path.pdf")
            self.assertIn("Error in PDF extraction: Failed to open PDF", str(context.exception))

    def test_ocr_pdf_data_success(self):
        # Mocking convert_from_path and pytesseract.image_to_string
        with patch("pdf2image.convert_from_path", MagicMock(return_value=[MagicMock()])):
            with patch("pytesseract.image_to_string", return_value="OCR text"):
                result = ocr_pdf_data("dummy_path.pdf")
                self.assertEqual(result, "OCR text")

    def test_ocr_pdf_data_failure(self):
        with patch("pdf2image.convert_from_path", side_effect=Exception("Conversion failed")):
            with self.assertRaises(RuntimeError) as context:
                ocr_pdf_data("bad_path.pdf")
            self.assertIn("Error in OCR process: Conversion failed", str(context.exception))

    def test_compare_results(self):
        self.assertEqual(compare_results("Text longer", "short"), "Text longer")
        self.assertEqual(compare_results(None, "fallback"), "fallback")
        self.assertIsNone(compare_results(None, None))

    def test_process_pdf_integration(self):
        # Integration test for process_pdf, mocks all called methods
        with patch("your_module.extract_pdf_data", return_value="Extracted data"):
            with patch("your_module.ocr_pdf_data", return_value="OCR data longer"):
                result = process_pdf("dummy_path.pdf")
                self.assertEqual(result, "OCR data longer")

if __name__ == "__main__":
    unittest.main()
