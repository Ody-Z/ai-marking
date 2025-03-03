import os
import logging
from pathlib import Path
from markitdown import MarkItDown

logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Uses Microsoft MarkItDown to convert PDFs to Markdown.
    """

    def __init__(self, enable_plugins=False, docintel_endpoint=None, llm_client=None, llm_model=None):
        """
        Initialize the PDF Processor with MarkItDown.

        Args:
            enable_plugins (bool): Whether to enable MarkItDown plugins (not used in 0.0.1a5)
            docintel_endpoint (str, optional): Azure Document Intelligence endpoint
            llm_client (object, optional): LLM client for enhanced image descriptions
            llm_model (str, optional): LLM model name for enhanced image descriptions
        """
        logger.info("Initializing PDF Processor with MarkItDown API")
        # In version 0.0.1a5, MarkItDown doesn't support these parameters
        self.markitdown = MarkItDown()

        # Store parameters for future use if needed
        self.enable_plugins = enable_plugins
        self.docintel_endpoint = docintel_endpoint
        self.llm_client = llm_client
        self.llm_model = llm_model

    def pdf_to_markdown(self, pdf_path):
        """
        Convert a PDF file to Markdown using Microsoft MarkItDown.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Markdown content generated from the PDF
        """
        logger.info(
            f"Converting PDF to Markdown using MarkItDown API: {pdf_path}")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Use MarkItDown Python API to convert PDF to Markdown
            result = self.markitdown.convert(pdf_path)
            markdown_content = result.text_content

            logger.info(
                f"Successfully converted PDF to Markdown: {len(markdown_content)} characters")
            return markdown_content

        except Exception as e:
            logger.error(f"Error converting PDF to Markdown: {str(e)}")
            raise
