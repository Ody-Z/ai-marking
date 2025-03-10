import os
import shutil
from fastapi import UploadFile
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.config import UPLOAD_FOLDER

logger = logging.getLogger(__name__)


async def save_upload_file(upload_file: UploadFile, filename: str) -> str:
    """
    Save an uploaded file to the upload folder.

    Args:
        upload_file (UploadFile): The uploaded file
        filename (str): Desired filename

    Returns:
        str: Path to the saved file
    """
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Create a file with the same name
        with open(file_path, "wb") as f:
            # Read the uploaded file in chunks to handle large files
            content = await upload_file.read()
            f.write(content)

        logger.info(f"Successfully saved file to {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"Error saving file {filename}: {str(e)}")
        raise e


def create_feedback_pdf(output_path, feedback, marks, student_name, assignment_title):
    """
    Generate a PDF with feedback and marks.

    Args:
        output_path (str): Path where to save the PDF
        feedback (str): Feedback text
        marks (str/float): Marks or grade
        student_name (str): Name of the student
        assignment_title (str): Title of the assignment
    """
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading1"]
        normal_style = styles["Normal"]

        # Custom styles
        mark_style = ParagraphStyle(
            "MarkStyle",
            parent=heading_style,
            textColor=colors.blue,
            fontSize=14
        )

        # Content elements
        elements = []

        # Title
        elements.append(
            Paragraph(f"Feedback: {assignment_title}", title_style))
        elements.append(Spacer(1, 12))

        # Student info
        elements.append(Paragraph(f"Student: {student_name}", heading_style))
        elements.append(Spacer(1, 12))

        # Marks
        elements.append(Paragraph(f"Mark: {marks}", mark_style))
        elements.append(Spacer(1, 24))

        # Feedback
        elements.append(Paragraph("Detailed Feedback:", heading_style))
        elements.append(Spacer(1, 12))

        # Split feedback by paragraphs and add each as a paragraph element
        for para in feedback.split('\n'):
            if para.strip():
                elements.append(Paragraph(para, normal_style))
                elements.append(Spacer(1, 6))

        # Build PDF
        doc.build(elements)
        logger.info(f"Successfully created feedback PDF at {output_path}")

    except Exception as e:
        logger.error(f"Error creating feedback PDF: {str(e)}")
        raise e
