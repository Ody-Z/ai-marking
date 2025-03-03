import os
import logging
import tempfile
from pathlib import Path
import markdown
from weasyprint import HTML

logger = logging.getLogger(__name__)

class MarkdownToPDF:
    """
    Converts Markdown content to PDF files.
    """
    
    def __init__(self):
        logger.info("Initializing Markdown to PDF converter")
    
    def convert(self, markdown_content, output_path, title=None, css=None):
        """
        Convert Markdown content to a PDF file.
        
        Args:
            markdown_content (str): Markdown content to convert
            output_path (str): Path where to save the PDF
            title (str, optional): Title for the PDF document
            css (str, optional): Custom CSS for styling
            
        Returns:
            str: Path to the generated PDF file
        """
        logger.info(f"Converting Markdown to PDF, output: {output_path}")
        
        try:
            # Convert markdown to HTML
            html_content = markdown.markdown(
                markdown_content,
                extensions=['extra', 'codehilite', 'tables']
            )
            
            # Add HTML document structure with optional title and CSS
            html_document = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{title or 'Feedback Document'}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 2cm;
                    }}
                    h1, h2, h3, h4, h5, h6 {{
                        color: #2c3e50;
                        margin-top: 1.5em;
                        margin-bottom: 0.5em;
                    }}
                    h1 {{ font-size: 2em; }}
                    h2 {{ font-size: 1.5em; }}
                    pre {{
                        background-color: #f5f5f5;
                        padding: 1em;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                    code {{
                        background-color: #f5f5f5;
                        padding: 0.2em 0.4em;
                        border-radius: 3px;
                    }}
                    blockquote {{
                        border-left: 4px solid #ccc;
                        padding-left: 1em;
                        margin-left: 0;
                        color: #555;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 1em 0;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        text-align: left;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    {css or ''}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Create parent directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Convert HTML to PDF using WeasyPrint
            HTML(string=html_document).write_pdf(output_path)
            
            logger.info(f"Successfully created PDF at {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error converting Markdown to PDF: {str(e)}")
            raise 