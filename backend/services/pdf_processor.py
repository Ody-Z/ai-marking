import os
import logging
from pathlib import Path
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Uses marker to convert PDFs to Markdown.
    """

    def __init__(self, enable_plugins=False, docintel_endpoint=None, llm_client=None, llm_model=None):
        """
        Initialize the PDF Processor with marker.

        Args:
            enable_plugins (bool): Whether to enable plugins (not used)
            docintel_endpoint (str, optional): Azure Document Intelligence endpoint (not used)
            llm_client (object, optional): LLM client for enhanced processing
            llm_model (str, optional): LLM model name
        """
        logger.info("Initializing PDF Processor with marker")

        # Initialize marker converter
        self.converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )

        # Store parameters for future use if needed
        self.enable_plugins = enable_plugins
        self.docintel_endpoint = docintel_endpoint
        self.llm_client = llm_client
        self.llm_model = llm_model

    def pdf_to_markdown(self, pdf_path):
        """
        Convert a PDF file to Markdown using marker.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Markdown content generated from the PDF
        """
        logger.info(f"Converting PDF to Markdown using marker: {pdf_path}")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Convert PDF to Markdown using marker
            rendered = self.converter(
                pdf_path, use_llm=self.llm_client is not None)
            markdown_content, _, _ = text_from_rendered(rendered)

            logger.info(
                f"Successfully converted PDF to Markdown: {len(markdown_content)} characters")
            return markdown_content

        except Exception as e:
            logger.error(f"Error converting PDF to Markdown: {str(e)}")
            raise
