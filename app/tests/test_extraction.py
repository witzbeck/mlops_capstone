from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from app.__init__ import docstore
from app.extract import (
    compare_results,
    extract_pdf_data,
    ocr_pdf_data,
    process_pdf,
)


class TestExtractData(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.test_pdf_path = docstore / "documents/ACORD_CA_APP.pdf"

    def test_doc_path(self):
        self.assertTrue(docstore.exists())
        self.assertTrue(self.test_pdf_path.exists())

    def test_process_template_pdf(self):
        result = extract_pdf_data(self.test_pdf_path)
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

    def test_extract_pdf_data_failure(self):
        # Simulate an exception during PDF reading
        with patch(
            "pdfplumber.open",
            MagicMock(
                return_value=MagicMock(
                    pages=[MagicMock(extract_text=MagicMock(return_value="text"))]
                )
            ),
        ):
            with self.assertRaises(RuntimeError) as context:
                extract_pdf_data("faulty_path.pdf")
            self.assertIn("PDF file not found", str(context.exception))
            self.assertIn(
                "No such file or directory: 'faulty_path.pdf'", str(context.exception)
            )


class TestOCRExtraction(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.test_pdf_path = docstore / "documents/ACORD_CA_APP.pdf"

    def test_doc_path(self):
        self.assertTrue(docstore.exists())
        self.assertTrue(self.test_pdf_path.exists())

    def test_ocr_pdf_data_success(self):
        # Mock pytesseract to simulate OCR without executing the external command
        result = ocr_pdf_data(self.test_pdf_path)
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
                ocr_pdf_data("bad_path.pdf")
            self.assertIn("Error in OCR process:", str(context.exception))


class TestPDFProcessing(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.test_pdf_path = docstore / "documents/ACORD_CA_APP.pdf"

    def test_doc_path(self):
        self.assertTrue(docstore.exists())
        self.assertTrue(self.test_pdf_path.exists())

    def test_compare_results(self):
        self.assertEqual(compare_results("Text longer", "short"), "Text longer")
        self.assertEqual(compare_results(None, "fallback"), "fallback")
        self.assertIsNone(compare_results(None, None))

    def test_mock_process_pdf_integration(self):
        with (
            patch("app.extract.extract_pdf_data", return_value="Extracted data"),
            patch("app.extract.ocr_pdf_data", return_value="OCR data"),
        ):
            result = process_pdf("dummy_path.pdf", use_multiprocessing=False)
            self.assertEqual(
                result, "Extracted data"
            )  # Extracted data is longer than OCR data


if __name__ == "__main__":
    main()
