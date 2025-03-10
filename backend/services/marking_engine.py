from backend.services.pdf_processor import PDFProcessor
from backend.services.llm_service import LLMService
from backend.services.md_to_pdf import MarkdownToPDF
import os
import sys
import logging
import tempfile
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))

logger = logging.getLogger(__name__)


class MarkingEngine:
    """
    Orchestrates the workflow for marking homework:
    1. PDF to Markdown conversion
    2. LLM processing for feedback generation
    3. Markdown to PDF conversion for final output
    """

    def __init__(self, enable_plugins=False, docintel_endpoint=None):
        """
        Initialize the Marking Engine.

        Args:
            enable_plugins (bool): Whether to enable MarkItDown plugins
            docintel_endpoint (str, optional): Azure Document Intelligence endpoint
        """
        logger.info("Initializing Marking Engine")
        self.pdf_processor = PDFProcessor(
            enable_plugins=enable_plugins,
            docintel_endpoint=docintel_endpoint
        )
        self.llm_service = LLMService()
        self.md_to_pdf = MarkdownToPDF()

    async def process_submission(self, criteria_path, homework_path, output_path,
                                 student_name=None, assignment_title=None):
        """
        Process a submission by converting PDFs to Markdown, generating feedback, 
        and converting the feedback to PDF.

        Args:
            criteria_path (str): Path to the marking criteria PDF
            homework_path (str): Path to the student homework PDF
            output_path (str): Path where to save the output PDF
            student_name (str, optional): Name of the student
            assignment_title (str, optional): Title of the assignment

        Returns:
            str: Path to the generated feedback PDF
        """
        logger.info(
            f"Processing submission for {student_name or 'Unknown Student'}")

        try:
            # Step 1: Convert PDFs to Markdown
            logger.info("Step 1: Converting PDFs to Markdown")
            criteria_md = self.pdf_processor.pdf_to_markdown(criteria_path)
            homework_md = self.pdf_processor.pdf_to_markdown(homework_path)

            # Step 2: Generate feedback using LLM
            logger.info("Step 2: Generating feedback using LLM")
            feedback_md, marks = self.llm_service.generate_feedback(
                criteria_md, homework_md)

            # Step 3: Add header information to feedback Markdown
            feedback_md = self._add_header_to_feedback(
                feedback_md,
                student_name or "Unknown Student",
                assignment_title or "Untitled Assignment",
                marks
            )

            # Step 4: Convert feedback Markdown to PDF
            logger.info("Step 3: Converting feedback Markdown to PDF")
            self.md_to_pdf.convert(
                feedback_md,
                output_path,
                title=f"Feedback: {assignment_title or 'Homework Assignment'}"
            )

            logger.info(
                f"Successfully processed submission, output saved to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error processing submission: {str(e)}")
            self._generate_error_report(output_path, str(
                e), student_name, assignment_title)
            raise

    def _add_header_to_feedback(self, feedback_md, student_name, assignment_title, marks):
        """Add a header to the feedback Markdown"""
        header = f"""# Feedback: {assignment_title}

**Student:** {student_name}

**Mark:** {marks}

---

"""
        return header + feedback_md

    def _generate_error_report(self, output_path, error_message, student_name, assignment_title):
        """Generate an error report PDF if processing fails"""
        try:
            error_md = f"""# Error Processing Submission

**Student:** {student_name or "Unknown Student"}
**Assignment:** {assignment_title or "Untitled Assignment"}

## Error Details

An error occurred while processing this submission:

{error_message}

Please contact technical support for assistance.
"""
            self.md_to_pdf.convert(error_md, output_path, title="Error Report")
            logger.info(f"Error report saved to {output_path}")
        except Exception as e:
            logger.error(f"Error generating error report: {str(e)}")
            raise
