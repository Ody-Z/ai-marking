from marker.models import create_model_dict  # Add this import

import unittest
import os
import tempfile
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
from reportlab.pdfgen import canvas

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))

from backend.services.pdf_processor import PDFProcessor


@patch('backend.services.pdf_processor.PdfConverter')  # Class-level patch
class TestPDFProcessor(unittest.TestCase):
    """
    Test cases for the PDFProcessor class.
    """

    def setUp(self):
        """Set up test fixtures before each test method is run."""
        # Create a temporary test directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a valid test PDF file
        self.test_pdf_path = os.path.join(self.temp_dir.name, "test.pdf")
        self._create_test_pdf(self.test_pdf_path)

    def _create_test_pdf(self, path):
        """Create a valid PDF file for testing."""
        c = canvas.Canvas(path)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(
            100, 700, "This is a test PDF file created for unit testing.")
        c.save()

    def tearDown(self):
        """Clean up test fixtures after each test method is run."""
        self.temp_dir.cleanup()

    def test_init(self, mock_converter):
        """Test PDFProcessor initialization."""
        # Mock create_model_dict
        with patch('backend.services.pdf_processor.create_model_dict') as mock_create_model_dict:
            mock_dict = {'mock': 'dict'}
            mock_create_model_dict.return_value = mock_dict

            processor = PDFProcessor(
                enable_plugins=True,
                docintel_endpoint="test_endpoint",
                llm_client="test_client",
                llm_model="test_model"
            )

            # Check if PdfConverter was initialized correctly
            mock_converter.assert_called_once_with(
                artifact_dict=mock_dict
            )

            # Check if parameters were stored
            self.assertTrue(processor.enable_plugins)
            self.assertEqual(processor.docintel_endpoint, "test_endpoint")
            self.assertEqual(processor.llm_client, "test_client")
            self.assertEqual(processor.llm_model, "test_model")

    def test_pdf_to_markdown_success(self, mock_converter):
        """Test successful PDF to Markdown conversion."""
        # Setup mock
        mock_instance = mock_converter.return_value
        mock_rendered = MagicMock()
        mock_instance.return_value = mock_rendered

        # Mock text_from_rendered function
        expected_markdown = "# Test Markdown\n\nThis is a test."
        with patch('backend.services.pdf_processor.text_from_rendered') as mock_text_from_rendered:
            mock_text_from_rendered.return_value = (
                expected_markdown, None, None)

            # Create processor instance and call method
            processor = PDFProcessor()
            result = processor.pdf_to_markdown(self.test_pdf_path)

            # Verify the result
            self.assertEqual(result, expected_markdown)
            mock_instance.assert_called_once_with(
                self.test_pdf_path, use_llm=False)  # Add use_llm parameter
            mock_text_from_rendered.assert_called_once_with(mock_rendered)

    def test_pdf_to_markdown_file_not_found(self, mock_converter):
        """Test PDF to Markdown conversion with non-existent file."""
        processor = PDFProcessor()
        non_existent_path = os.path.join(
            self.temp_dir.name, "non_existent.pdf")

        # Verify that FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            processor.pdf_to_markdown(non_existent_path)

    def test_pdf_to_markdown_conversion_error(self, mock_converter):
        """Test PDF to Markdown conversion with error."""
        # Setup mock to raise an exception
        mock_instance = mock_converter.return_value
        mock_instance.side_effect = Exception("Conversion error")

        # Create processor instance after setting up mock
        processor = PDFProcessor()

        # Verify that the exception is propagated
        with self.assertRaises(Exception) as context:
            processor.pdf_to_markdown(self.test_pdf_path)

        self.assertIn("Conversion error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
