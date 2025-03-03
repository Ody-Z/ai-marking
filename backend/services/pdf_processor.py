import os
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Uses Microsoft MarkItDown to convert PDFs to Markdown.
    """
    
    def __init__(self):
        logger.info("Initializing PDF Processor with MarkItDown")
        self._check_markitdown_installed()
    
    def _check_markitdown_installed(self):
        """Verify MarkItDown CLI is installed and accessible"""
        try:
            result = subprocess.run(
                ["markitdown", "--version"], 
                capture_output=True, 
                text=True
            )
            logger.info(f"MarkItDown version: {result.stdout.strip()}")
        except FileNotFoundError:
            logger.warning("MarkItDown not found in PATH. Make sure it's installed correctly.")
    
    def pdf_to_markdown(self, pdf_path):
        """
        Convert a PDF file to Markdown using Microsoft MarkItDown.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Path to the generated Markdown file
        """
        logger.info(f"Converting PDF to Markdown: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Create a temporary directory for the output
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, "output.md")
                
                # Run MarkItDown CLI to convert PDF to Markdown
                result = subprocess.run(
                    ["markitdown", "convert", pdf_path, "--output", output_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    raise Exception(f"MarkItDown conversion failed: {result.stderr}")
                
                # Read the markdown content
                with open(output_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()
                
                logger.info(f"Successfully converted PDF to Markdown: {len(markdown_content)} characters")
                return markdown_content
        
        except Exception as e:
            logger.error(f"Error converting PDF to Markdown: {str(e)}")
            raise 