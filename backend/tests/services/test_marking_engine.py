import unittest
import os
import tempfile
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))

# Mock weasyprint before importing any modules that use it
sys.modules['weasyprint'] = MagicMock()

from backend.services.marking_engine import MarkingEngine


class TestMarkingEngine(unittest.TestCase):
    """
    Test cases for the MarkingEngine class.
    """

    def setUp(self):
        """Set up test fixtures before each test method is run."""
        # Create a temporary test directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create test file paths
        self.criteria_path = os.path.join(self.temp_dir.name, "criteria.pdf")
        self.homework_path = os.path.join(self.temp_dir.name, "homework.pdf")
        self.output_path = os.path.join(self.temp_dir.name, "feedback.pdf")

        # Create empty test files
        Path(self.criteria_path).touch()
        Path(self.homework_path).touch()

    def tearDown(self):
        """Clean up test fixtures after each test method is run."""
        self.temp_dir.cleanup()

    @patch('backend.services.marking_engine.PDFProcessor')
    @patch('backend.services.marking_engine.LLMService')
    @patch('backend.services.marking_engine.MarkdownToPDF')
    def test_init(self, mock_md_to_pdf, mock_llm_service, mock_pdf_processor):
        """Test MarkingEngine initialization."""
        engine = MarkingEngine(enable_plugins=True,
                               docintel_endpoint="test_endpoint")

        # Check if services were initialized correctly
        mock_pdf_processor.assert_called_once_with(
            enable_plugins=True,
            docintel_endpoint="test_endpoint"
        )
        mock_llm_service.assert_called_once()
        mock_md_to_pdf.assert_called_once()

    @patch('backend.services.marking_engine.PDFProcessor')
    @patch('backend.services.marking_engine.LLMService')
    @patch('backend.services.marking_engine.MarkdownToPDF')
    async def test_process_submission_success(self, mock_md_to_pdf, mock_llm_service, mock_pdf_processor):
        """Test successful submission processing."""
        # Setup mocks
        mock_pdf_instance = mock_pdf_processor.return_value
        mock_llm_instance = mock_llm_service.return_value
        mock_md_to_pdf_instance = mock_md_to_pdf.return_value

        # Mock PDF to Markdown conversion
        mock_pdf_instance.pdf_to_markdown.side_effect = [
            "# Criteria\nTest criteria",  # criteria_md
            "# Homework\nTest homework"   # homework_md
        ]

        # Mock LLM feedback generation
        mock_llm_instance.generate_feedback = AsyncMock(
            return_value=("# Feedback\nGood work!", 85)
        )

        # Create engine and process submission
        engine = MarkingEngine()
        result = await engine.process_submission(
            self.criteria_path,
            self.homework_path,
            self.output_path,
            student_name="Test Student",
            assignment_title="Test Assignment"
        )

        # Verify the workflow
        mock_pdf_instance.pdf_to_markdown.assert_any_call(self.criteria_path)
        mock_pdf_instance.pdf_to_markdown.assert_any_call(self.homework_path)
        mock_llm_instance.generate_feedback.assert_called_once_with(
            "# Criteria\nTest criteria",
            "# Homework\nTest homework"
        )
        mock_md_to_pdf_instance.convert.assert_called_once()
        self.assertEqual(result, self.output_path)

    @patch('backend.services.marking_engine.PDFProcessor')
    @patch('backend.services.marking_engine.LLMService')
    @patch('backend.services.marking_engine.MarkdownToPDF')
    async def test_process_submission_error(self, mock_md_to_pdf, mock_llm_service, mock_pdf_processor):
        """Test submission processing with error."""
        # Setup mock to raise an exception
        mock_pdf_instance = mock_pdf_processor.return_value
        mock_pdf_instance.pdf_to_markdown.side_effect = Exception(
            "Conversion error")

        # Create engine
        engine = MarkingEngine()

        # Verify that the exception is propagated and error report is generated
        with self.assertRaises(Exception) as context:
            await engine.process_submission(
                self.criteria_path,
                self.homework_path,
                self.output_path,
                student_name="Test Student",
                assignment_title="Test Assignment"
            )

        self.assertIn("Conversion error", str(context.exception))
        # Error report should be generated
        mock_md_to_pdf.return_value.convert.assert_called_once()

    def test_add_header_to_feedback(self):
        """Test adding header to feedback markdown."""
        engine = MarkingEngine()
        feedback_md = "Test feedback content"
        result = engine._add_header_to_feedback(
            feedback_md,
            "Test Student",
            "Test Assignment",
            85
        )

        # Verify header content
        self.assertIn("# Feedback: Test Assignment", result)
        self.assertIn("**Student:** Test Student", result)
        self.assertIn("**Mark:** 85", result)
        self.assertIn("Test feedback content", result)

    @patch('backend.services.marking_engine.MarkdownToPDF')
    def test_generate_error_report(self, mock_md_to_pdf):
        """Test error report generation."""
        engine = MarkingEngine()
        engine._generate_error_report(
            self.output_path,
            "Test error message",
            "Test Student",
            "Test Assignment"
        )

        # Verify error report generation
        mock_md_to_pdf.return_value.convert.assert_called_once()
        call_args = mock_md_to_pdf.return_value.convert.call_args[0]
        error_md = call_args[0]

        # Check error report content
        self.assertIn("# Error Processing Submission", error_md)
        self.assertIn("**Student:** Test Student", error_md)
        self.assertIn("**Assignment:** Test Assignment", error_md)
        self.assertIn("Test error message", error_md)


if __name__ == "__main__":
    unittest.main()
