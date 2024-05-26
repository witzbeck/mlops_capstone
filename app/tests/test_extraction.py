from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from app.__init__ import DOCSTORE_PATH
from app.extract import (
    compare_results,
    extract_pdf_data,
    extract_ocr_data,
    process_pdf,
)


TEST_PDF_PATH = DOCSTORE_PATH / "ACORD_CA_APP.pdf"


class TestPaths(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.test_pdf_path = TEST_PDF_PATH

    def test_doc_path(self):
        self.assertTrue(DOCSTORE_PATH.exists())
        self.assertTrue(self.test_pdf_path.exists())


class TestExtractData(TestCase):
    def test_process_template_pdf(self):
        result = extract_pdf_data(TEST_PDF_PATH)
        self.assertTrue(result)
        self.assertIsInstance(result, str)
        self.assertIn("ACORD", result)
        self.assertIn("COMMERCIAL INSURANCE APPLICATION", result)
        self.assertIn("POLICY NUMBER", result)

    def test_extract_pdf_data_success(self):
        # Properly mock pdfplumber.open to return a realistic mock
        with (
            patch("app.extract.extract_pdf_data", return_value="Extracted data"),
        ):
            with patch("app.extract.open_pdf", MagicMock()) as mock_pdf:
                mock_pdf.return_value.__enter__.return_value.pages = [
                    MagicMock(extract_text=MagicMock(return_value="This is a test."))
                ]
                result = extract_pdf_data("dummy_path.pdf")
                self.assertEqual(result, "This is a test.")

    @patch(
        "pdfplumber.open",
        MagicMock(
            side_effect=FileNotFoundError(
                "[Errno 2] No such file or directory: 'faulty_path.pdf'"
            )
        ),
    )
    def test_extract_pdf_data_failure(self):
        with self.assertRaises(RuntimeError) as context:
            extract_pdf_data("faulty_path.pdf")
        self.assertIn("PDF file not found", str(context.exception))


class TestOCRExtraction(TestCase):
    def test_ocr_pdf_data_success(self):
        # Mock pytesseract to simulate OCR without executing the external command
        result = extract_ocr_data(TEST_PDF_PATH)
        self.assertTrue(result)
        self.assertIsInstance(result, str)
        self.assertIn("ACORD", result)
        self.assertIn("COMMERCIAL INSURANCE APPLICATION", result)
        self.assertIn("POLICY NUMBER", result)

    def test_ocr_pdf_data_failure(self):
        with patch(
            "pdf2image.convert_from_path", side_effect=Exception("Conversion failed")
        ):
            with self.assertRaises(RuntimeError) as context:
                extract_ocr_data("bad_path.pdf")
            self.assertIn("Error in OCR process:", str(context.exception))


class TestPDFProcessing(TestCase):
    def test_compare_results(self):
        self.assertEqual(compare_results("Text longer", "short"), "Text longer")
        self.assertEqual(compare_results(None, "fallback"), "fallback")
        self.assertIsNone(compare_results(None, None))

    def test_mock_process_pdf_integration(self):
        with self.assertRaises(FileNotFoundError):
            process_pdf("non_existent_path.pdf")


if __name__ == "__main__":
    main()
